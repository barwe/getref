import os
import sys

sys.path.append(os.path.dirname(__file__))
from src.researchgate import ResearchGate

def log(msg, verbose=True):
    if verbose:
        print(msg)       
       
if __name__ == '__main__':
    
    output_dir = input('Set output directory (default References/): ').strip()
    if not output_dir:
        output_dir = 'References'
    rg = ResearchGate(output_dir = output_dir)
    
    # 交互式
    if len(sys.argv) == 1:
        while True:
            print('-' * 20)
            print('Input q/quit/e/exit or press Ctrl+C to exit!')
            title = input('Your title: ').strip()
            if title in ('q', 'quit', 'e', 'exit'):
                break
            else:
                rg.get(title)
        
    else:
        fp = sys.argv[1]
        if os.path.exists(fp):
            titles = [i for i in open(fp).read().strip().split('\n') if i]
            for title in titles:
                print('-' * 20)
                print(title)
                rg.get(title)
        else:
            log('File not found: "%s"' % fp)