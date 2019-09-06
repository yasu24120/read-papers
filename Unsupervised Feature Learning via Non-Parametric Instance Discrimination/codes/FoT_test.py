import torch
import time
import datasets
from lib.utils import AverageMeter
import torchvision.transforms as transforms
import numpy as np

def NN(epoch, net, lemniscate, trainloader, testloader, recompute_memory=0):
    net.eval()
    net_time = AverageMeter()
    cls_time = AverageMeter()
    losses = AverageMeter()
    correct = 0.
    total = 0
    testsize = testloader.dataset.__len__()

    trainFeatures = lemniscate.memory.t()
    if hasattr(trainloader.dataset, 'imgs'):
        trainLabels = torch.LongTensor([y for (p, y) in trainloader.dataset.imgs]).cuda()
    else:
        trainLabels = torch.LongTensor(trainloader.dataset.targets).cuda()
            #trainLabels = torch.LongTensor(trainloader.dataset.train_labels).cuda()

    if recompute_memory:
        transform_bak = trainloader.dataset.transform
        trainloader.dataset.transform = testloader.dataset.transform
        temploader = torch.utils.data.DataLoader(trainloader.dataset, batch_size=100, shuffle=False, num_workers=1)
        for batch_idx, (inputs, targets, indexes) in enumerate(temploader):
            targets = targets.cuda() #targets = targets.cuda(async=True)
            batchSize = inputs.size(0)
            features = net(inputs)
            trainFeatures[:, batch_idx*batchSize:batch_idx*batchSize+batchSize] = features.data.t() ### trainFeatures (DB的なリスト)を取得
        trainLabels = torch.LongTensor(temploader.dataset.targets).cuda()
            #trainLabels = torch.LongTensor(temploader.dataset.train_labels).cuda()
        trainloader.dataset.transform = transform_bak
    
    end = time.time()
    with torch.no_grad():
        for batch_idx, (inputs, targets, indexes) in enumerate(testloader):
            targets = targets.cuda() #targets = targets.cuda(async=True)
            batchSize = inputs[0].size(0)
            
            ### inputsの特徴fiを抽出
            for _ind, inp in enumerate(inputs):
                feature = net(inp)
                if _ind==0:
                    features = feature
                else:
                    features = torch.cat((features, feature),-1)

            net_time.update(time.time() - end)
            end = time.time()

            dist = torch.mm(features, trainFeatures) ###fiとlemniscate内のweightのコサイン類似度を計算

            yd, yi = dist.topk(1, dim=1, largest=True, sorted=True) ### top1のindex (yi) を持ってくる
            candidates = trainLabels.view(1,-1).expand(batchSize, -1) ###ラベルのリストをもってくる
            retrieval = torch.gather(candidates, 1, yi) ###リストの内、yiを取得する

            retrieval = retrieval.narrow(1, 0, 1).clone().view(-1)
            yd = yd.narrow(1, 0, 1)

            total += targets.size(0)
            correct += retrieval.eq(targets.data).sum().item()
            
            cls_time.update(time.time() - end)
            end = time.time()

        print('Test [{}/{}]\t'
                  'Net Time {net_time.val:.3f} ({net_time.avg:.3f})\t'
                  'Cls Time {cls_time.val:.3f} ({cls_time.avg:.3f})\t'
                  'Top1: {:.2f}'.format(
                  total, testsize, correct*100./total, net_time=net_time, cls_time=cls_time))

    return correct/total

def kNN(epoch, net, lemniscate, trainloader, testloader, K, sigma, recompute_memory=0):
    net.eval()
    net_time = AverageMeter()
    cls_time = AverageMeter()
    total = 0
    testsize = testloader.dataset.__len__()

    trainFeatures = lemniscate.memory.t()
    if hasattr(trainloader.dataset, 'imgs'):
        trainLabels = torch.LongTensor([y for (p, y) in trainloader.dataset.imgs]).cuda()
    else:
        trainLabels = torch.LongTensor(trainloader.dataset.targets).cuda()
            #trainLabels = torch.LongTensor(trainloader.dataset.train_labels).cuda()
    C = trainLabels.max() + 1

    if recompute_memory:
        transform_bak = trainloader.dataset.transform
        trainloader.dataset.transform = testloader.dataset.transform
        temploader = torch.utils.data.DataLoader(trainloader.dataset, batch_size=100, shuffle=False, num_workers=1)
        for batch_idx, (inputs, targets, indexes) in enumerate(temploader):
            targets = targets.cuda()
            batchSize = inputs.size(0)
            features = net(inputs)
            trainFeatures[:, batch_idx*batchSize:batch_idx*batchSize+batchSize] = features.data.t()
        trainLabels = torch.LongTensor(temploader.dataset.targets).cuda()
            #trainLabels = torch.LongTensor(temploader.dataset.train_labels).cuda()
        trainloader.dataset.transform = transform_bak
    
    top1 = 0.
    top5 = 0.
    end = time.time()
    with torch.no_grad():
        retrieval_one_hot = torch.zeros(K, C).cuda()
        for batch_idx, (inputs, targets, indexes) in enumerate(testloader):
            end = time.time()
            targets = targets.cuda()
            batchSize = inputs[0].size(0)
            
            ### inputsの特徴fiを抽出
            for _ind, inp in enumerate(inputs):
                feature = net(inp)
                if _ind==0:
                    features = feature
                else:
                    features = torch.cat((features, feature),-1)
            #features = net(inputs)
            net_time.update(time.time() - end)
            end = time.time()

            dist = torch.mm(features, trainFeatures)   

            yd, yi = dist.topk(K, dim=1, largest=True, sorted=True)
            candidates = trainLabels.view(1,-1).expand(batchSize, -1)
            retrieval = torch.gather(candidates, 1, yi)

            retrieval_one_hot.resize_(batchSize * K, C).zero_()
            retrieval_one_hot.scatter_(1, retrieval.view(-1, 1), 1)
            yd_transform = yd.clone().div_(sigma).exp_()
            probs = torch.sum(torch.mul(retrieval_one_hot.view(batchSize, -1 , C), yd_transform.view(batchSize, -1, 1)), 1)
            _, predictions = probs.sort(1, True)

            # Find which predictions match the target
            correct = predictions.eq(targets.data.view(-1,1))
            cls_time.update(time.time() - end)

            top1 = top1 + correct.narrow(1,0,1).sum().item()
            top5 = top5 + correct.narrow(1,0,5).sum().item()

            total += targets.size(0)

        print('Test [{}/{}]\t'
                  'Net Time {net_time.val:.3f} ({net_time.avg:.3f})\t'
                  'Cls Time {cls_time.val:.3f} ({cls_time.avg:.3f})\t'
                  'Top1: {:.2f}  Top5: {:.2f}'.format(
                  total, testsize, top1*100./total, top5*100./total, net_time=net_time, cls_time=cls_time))


    return top1/total, top5/total

### 検索用の関数。魔改造
### 使い方の例 %run -i main.py  --resume pretrainedResnet18.pth.tar --retrieval ./datasets/retrieval
def retrieval(net, lemniscate, trainloader, retrievalloader, K, sigma, retrieval_dir,recompute_memory=0):
    net.eval()
    net_time = AverageMeter()
    cls_time = AverageMeter()
    total = 0
    retrievalsize = retrievalloader.dataset.__len__()

    trainFeatures = lemniscate.memory.t()
    if hasattr(trainloader.dataset, 'imgs'):
        trainLabels = torch.LongTensor([y for (p, y) in trainloader.dataset.imgs]).cuda()
    else:
        trainLabels = torch.LongTensor(trainloader.dataset.targets).cuda()
            #trainLabels = torch.LongTensor(trainloader.dataset.train_labels).cuda()
    C = trainLabels.max() + 1

    ### memory bankの再計算。基本的に使わないようにしたい
    if recompute_memory:
        transform_bak = trainloader.dataset.transform
        trainloader.dataset.transform = retrievalloader.dataset.transform
        temploader = torch.utils.data.DataLoader(trainloader.dataset, batch_size=100, shuffle=False, num_workers=1)
        for batch_idx, (inputs, targets, indexes) in enumerate(temploader):
            targets = targets.cuda()
            batchSize = inputs.size(0)
            features = net(inputs)
            trainFeatures[:, batch_idx*batchSize:batch_idx*batchSize+batchSize] = features.data.t()
        trainLabels = torch.LongTensor(temploader.dataset.targets).cuda()
            #trainLabels = torch.LongTensor(temploader.dataset.train_labels).cuda()
        trainloader.dataset.transform = transform_bak
        
    retrieved_dir = os.path.join(os.path.dirname(retrieval_dir), 'retrieved')
    if not os.path.isdir(retrieved_dir):
        os.mkdir(retrieved_dir)
        os.chmod(retrieved_dir, 0o777)
    
    end = time.time()
    with torch.no_grad():
        #retrieval_one_hot = torch.zeros(K, C).cuda()
        for batch_idx, (inputs, targets, indexes) in enumerate(retrievalloader):
            targets = targets.cuda()
            batchSize = inputs[0].size(0)
            
            ### inputsの特徴fiを抽出
            for _ind, inp in enumerate(inputs):
                feature = model(inp)
                if _ind==0:
                    features = inp
                else:
                    features = torch.cat((features, feature),-1)
            #features = net(inputs)

            dist = torch.mm(features, trainFeatures)   

            yd, yi = dist.topk(K, dim=1, largest=True, sorted=True)
            
            for x_ind in range(len(retrievalloader.dataset.imgs)):
                ###print(retrievalloader.dataset.imgs[x_ind][0])
                make_dir = os.path.basename(retrievalloader.dataset.imgs[x_ind][0])[:-5] ###.jpegを想定
                make_dir = os.path.join(retrieved_dir, make_dir)
                if os.path.isdir(make_dir):
                    shutil.rmtree(make_dir)
                os.mkdir(make_dir)
                os.chmod(make_dir, 0o777)
                for _k in range(K):
                    retrieval_key = int(yi[x_ind][_k])
                    ###print(trainloader.dataset.imgs[retrieval_key][0])
                    cpy_img_path = trainloader.dataset.imgs[retrieval_key][0]
                    cpy_img_name = os.path.basename(cpy_img_path)
                    cpy_img_name = os.path.join(make_dir, cpy_img_name)
                    shutil.copyfile(cpy_img_path, cpy_img_name)
        net_time.update(time.time() - end)
        print('elapsed time : {net_time.val:.3f}'.format(net_time=net_time) )
        return