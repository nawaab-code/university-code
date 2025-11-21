# Write a python program to implement the following using strings
# The third person singular verb form in English is distinguished by the suffix -s, which is added to the stem of the infinitive form: run -> runs. A simple set of rules can be given as follows:

# 1. If the verb ends in y, remove it and add ies
# 2. If the verb ends in o, ch, s, sh, x or z, add es
# 3. By default just add s
# 4. Test your function with words like try, brush, run and fix.

# Tip:Check out the string method endswith().

import string

def change(text):
    if text.endswith('y'):
        changed=text[:-1]+"ies"
    elif text.endswith('or') or text.endswith('ch') or text.endswith('s') or text.endswith('sh') or text.endswith('x') or text.endswith('z'):
        changed=text[:-1]+"es"
    else:
        changed=text[:-1]+"s"
    return changed

def main():
    text=input("Enter a verb:\t")
    print(f"The new word:\t{change(text)}")

main()