import torch
from torch.autograd import Function
from torch import nn
from .alias_multinomial import AliasMethod
import math

class NCEFunction(Function):
    @staticmethod
    def forward(self, x, y, memory, idx, params):  ### idx: [batch_size, K+1]    x:[batch,feature]
        K = int(params[0].item())    ### 論文のNCEにおけるm (number of negative samples)
        T = params[1].item()    ### 論文のNCEにおけるτ (temperature parameter)
        Z = params[2].item()    ### none 

        momentum = params[3].item()
        batchSize = x.size(0)  ### x:[batch,feature], 論文中のfi
        outputSize = memory.size(0)  ### データのサンプル数
        inputSize = memory.size(1)  ### 128: feature
        
        # sample positives & negatives
        idx.select(1,0).copy_(y.data)  ### y.data : positives, idxには適当なindexが入っているので、1列目をy.dataで置き換え

        # sample correspoinding weights
        weight = torch.index_select(memory, 0, idx.view(-1))  ### idxに対応するweightを選択 論文中のv
        weight.resize_(batchSize, K+1, inputSize)
        
        # inner product
        out = torch.bmm(weight, x.reshape(batchSize, inputSize, 1))
        #out = torch.bmm(weight, x.resize_(batchSize, inputSize, 1)) #out = torch.bmm(weight, x.data.resize_(batchSize, inputSize, 1))
        out.div_(T).exp_() # batchSize * self.K+1   ### [batch, k+1, 1]
        x.reshape(batchSize,inputSize)#x.resize_(batchSize,inputSize) #x.data.resize_(batchSize, inputSize)
        
        if Z < 0:   ### Eqn.8
            params[2] = out.mean() * outputSize  ### out.mean: 1/m sum(exp())   outputSize: n   として推定
            Z = params[2].item()
            print("normalization constant Z is set to {:.1f}".format(Z))

        out.div_(Z).resize_(batchSize, K+1)

        self.save_for_backward(x, memory, y, weight, out, params)

        return out

    @staticmethod
    def backward(self, gradOutput):
        x, memory, y, weight, out, params = self.saved_tensors
        K = int(params[0].item())
        T = params[1].item()
        Z = params[2].item()
        momentum = params[3].item()
        batchSize = gradOutput.size(0)
        
        # gradients d Pm / d linear = exp(linear) / Z
        gradOutput.data.mul_(out.data)
        # add temperature
        gradOutput.data.div_(T)

        gradOutput.resize_(batchSize, 1, K+1)#gradOutput.data.resize_(batchSize, 1, K+1)
        
        # gradient of linear
        gradInput = torch.bmm(gradOutput.data, weight)
        gradInput.resize_as_(x)

        # update the non-parametric data
        weight_pos = weight.select(1, 0).resize_as_(x)
        weight_pos.mul_(momentum)
        weight_pos.add_(torch.mul(x.data, 1-momentum))
        w_norm = weight_pos.pow(2).sum(1, keepdim=True).pow(0.5)
        updated_weight = weight_pos.div(w_norm)
        memory.index_copy_(0, y, updated_weight)
        
        return gradInput, None, None, None, None

class NCEAverage(nn.Module):

    def __init__(self, inputSize, outputSize, K, T=0.07, momentum=0.5, Z=None):
        super(NCEAverage, self).__init__()
        self.nLem = outputSize
        self.unigrams = torch.ones(self.nLem)
        self.multinomial = AliasMethod(self.unigrams)
        self.multinomial.cuda()
        self.K = K

        self.register_buffer('params',torch.tensor([K, T, -1, momentum]));
        stdv = 1. / math.sqrt(inputSize/3)
        self.register_buffer('memory', torch.rand(outputSize, inputSize).mul_(2*stdv).add_(-stdv))
 
    def forward(self, x, y):
        batchSize = x.size(0)
        idx = self.multinomial.draw(batchSize * (self.K+1)).view(batchSize, -1)
        out = NCEFunction.apply(x, y, self.memory, idx, self.params)
        return out

