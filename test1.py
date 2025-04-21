args = str(input('something : '))
getpos = [i for i,c in enumerate(args) if c == '"']
content = args[getpos[0]+1:] + args[getpos[1]:-1:]
print(content.removesuffix('"'))


# get_args = args.split()
# content = ''

# for i in get_args:
#     # print(i)
#     if '"' in i:
#         print(i.index('"'))
#     else:
#         continue



