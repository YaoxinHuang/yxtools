import torch_topological.nn as ttnn
from tools import timeit
from readers import file_reader
import torch

@timeit
def TopoLoss(seg_image, res_outputs):
    persistence_layer = ttnn.CubicalComplex()
    before_persistence_diagram = persistence_layer(seg_image)
    after_persistence_diagram = persistence_layer(res_outputs)
    distance = ttnn.WassersteinDistance()(before_persistence_diagram[0], after_persistence_diagram[0])
    return distance

if __name__ == '__main__':
    reader = file_reader()
    # shape = (633, 259, 352)
    seg, _, _, _ = reader(r"D:\Work\data\label.nii.gz")
    label, _, _, _ = reader(r"D:\Work\data\label.nii.gz")
    dis = TopoLoss(torch.asarray(seg*1.), torch.asarray(label*1.))
    print(dis)