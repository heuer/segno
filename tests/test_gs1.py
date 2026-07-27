# import sys
# sys.path.append(r"C:\Users\Willis\Desktop\segno\segno")


import segno

qr=segno.make("2100",version=1,gs1="first")
qr.show()

# https://www.gs1jp.org/assets/img/pdf/GS1_General_Specifications.pdf

# https://ref.gs1.org/ai/j
# AI_DATA_MAPPING = {
#     21: "N2+x..20"
# }

# GS1_CHARACTER_SET_82 = [

# ]

# #  page 155
# # n implied decimal point position
# # N numeric digit
# # X any character in figure 7.11-1 character set 82
# # N3 3 numeric digits, predefined length
# # X3 3 characters, fixed length
# # N..3 up to 3 numeric digits
# # X..3 up to 3 characters in figure 7.11-1
# # DD must be filled 

# AI_MAPPING = {
#     21: "N2+X..20"
# }


# def generate_gs1(string):
#     left_b_split=string.split("[",)
#     if left_b_split[0]:
#         raise ValueError(f'"string" must start with an AI in brackets "[]"')
#     ai_b_data=left_b_split[1:]
#     elements=[]
#     for i in range(len(ai_b_data)):
#         try:
#             ai,data=ai_b_data[i].split("]")
#         except:
#             raise ValueError(f'"string" contains open AI bracket')
#         if not ai.isdecimal():
#             raise ValueError("AI must be a whole number")
#         if not data.isalnum():
#             raise ValueError("Data must only contain characters 0-9, A-Z, and (#-/)")
#         print(ai, data)
#         elements.append((ai,data))
#     print(elements)

# generate_gs1("[21]00[21]00")