import re

expression = "f[3] + 3 +3.5 / (4+5) "

print(list(re.findall(r"[+\-*/()\[\]]|\d*\.\d+|\d+|\w+", expression)))