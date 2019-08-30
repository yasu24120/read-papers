import torch
from torch import nn

eps = 1e-7

class NCECriterion(nn.Module):

    def __init__(self, nLem):          ### nLem: number of data
        super(NCECriterion, self).__init__()
        self.nLem = nLem

    def forward(self, x, targets):    ### x: [batch, K+1]   targets: [batch], true indexが入っている
        batchSize = x.size(0)
        K = x.size(1)-1
        Pnt = 1 / float(self.nLem)
        Pns = 1 / float(self.nLem)
        
        # eq 5.1 : P(origin=model) = Pmt / (Pmt + k*Pnt) 
        Pmt = x.select(1,0)   ### xから、1列目を取り出す i.e. positive sample の確率,  Pmt=P(i|v)
        Pmt_div = Pmt.add(K * Pnt + eps)   ### Pnt = Pn(i)
        lnPmt = torch.div(Pmt, Pmt_div)
        
        # eq 5.2 : P(origin=noise) = k*Pns / (Pms + k*Pns)  = 1-Pms/(Pms + K*Pns)
        Pon_div = x.narrow(1,1,K).add(K * Pns + eps)   ### xから、1列目以外を取り出す i.e. negative sample の確率　→足す    [batch, K]
        Pon = Pon_div.clone().fill_(K * Pns)
        lnPon = torch.div(Pon, Pon_div)
     
        # equation 6 in ref. A
        lnPmt.log_()
        lnPon.log_()
        
        lnPmtsum = lnPmt.sum(0)
        lnPonsum = lnPon.view(-1, 1).sum(0)   ### view(-1,1) はkeras?でいうところのtoflatten()と同様
        
        loss = - (lnPmtsum + lnPonsum) / batchSize    ### lnPonsumに　m(K)をかけなくて良い？ → OK
        #loss = - (lnPmtsum + K*lnPonsum) / batchSize
        
        ### Proximal Regularizationは実装されていない
        
        return loss

