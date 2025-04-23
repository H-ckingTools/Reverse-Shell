args = str(input('something : '))
_args = args.split()
poses = []

for value,getpos in enumerate(_args):
    if '"' in getpos:
        poses.append(value)

content = ''
for i in range(poses[0],poses[1]+1):
    content += _args[i] + ' '

print(content.replace('"',''))


