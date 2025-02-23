

#configuration
import argparse
def get_config():
    parser = argparse.ArgumentParser()
    parser.add_argument('--batch_size', default=16, type=int, help='batch size of each gpu')
    parser.add_argument('--epochs', default=25, type=int)
    parser.add_argument('--cuda', default=0, type=int, help='GPU id')

    return parser.parse_args()
