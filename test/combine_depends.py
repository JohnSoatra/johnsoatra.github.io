#!python3
import json
import depends1
import depends2
import depends3

def save_to(save_path, depends):
    f = open(save_path, "w")
    f.write(
        json.dumps(
            depends,
            ensure_ascii=False,
            indent=4
        )
    )
    f.close()
    
    print('\n--- done ---')
    print('length = ', len(depends))
    print('-------------\n')

def main():
    ds = []
    
    for each in depends1.depends + depends2.depends + depends3.depends:
        if not each in ds:
            ds.append(each)
            
    ds.sort()
    save_to('combine.py', ds)

if __name__ == '__main__':
    main()