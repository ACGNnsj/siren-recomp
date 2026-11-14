import subprocess
nids = '''1cd9cfd 2170d1a 9ce84ac 15bae46b 1a91874b 24a1ea07 26f33146 2796fdf3 28b4e2c1 28e208bb 2c847572 350d454e 39a69619 3a33c1fd 3e22cb4b 3f09e20a 3f195b3a 3f72c56e 4357c77f 44f5c9e3 4e9bb95b 4f7172c9 619b1427 64f66d35 674bb9ff 6cb81eb2 6d087930 6db6e8cd 7208dc08 744680a2 749c9b5f 78d7f9ad 79225aa3 7fb3c6a5 8461e528 860b1756 88f03575 8d1d096c 93ced48d 967a162b 9949bf82 9ab20793 9c056962 a2d4189b a5f12145 a85a4951 a9a439e0 af3eba5a af57d9c9 aff080a4 b0a59804 b1c02d66 b202f0e8 b48636c4 b4c9b4f9 c94f6939 ca8181c1 cfd469e4 dabbc2c0 dc751b40 e22ed55d e2877bea e36c660e e90effea eb5f2544 ed4a0148 fba04f37 fcac355a fe669845'''.split()
with open('D:/consoles/ps3/siren/nids.txt', 'w') as f:
    f.write('\n'.join('0x' + n for n in nids) + '\n')
print('wrote', len(nids))
