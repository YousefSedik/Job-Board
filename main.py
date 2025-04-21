# from typing import List

# class Solution:
#     def countCompleteComponents(self, n: int, edges: List[List[int]]) -> int:
#         graph = [[] for _ in range(n)]
#         visited = set()
#         for u, v in edges:
#             graph[u].append(v)
#             graph[v].append(u)

#         def dfs(u, res):
#             visited.add(u)
#             for nei in graph[u]:
#                 if nei not in visited:
#                     res.append(nei)
#                     dfs(nei, res)
#             return res

#         number_of_components = 0
#         for i in range(n):
#             if i not in visited:
#                 component = dfs(i, [i])
#                 print(component)
#                 flag = True
#                 for v2 in component:
#                     if len(graph[v2]) != len(component) - 1:
#                         flag = False
#                         break
#                 if flag:
#                     number_of_components += 1

#         return number_of_components

# x =Solution()
# print(x.countCompleteComponents(n=6, edges=[[0, 1], [0, 2], [1, 2], [3, 4]]))

# print(x.countCompleteComponents(n=6, edges=[[0, 1], [0, 2], [1, 2], [3, 4], [3, 5]]))
# # opt. when false, make all as visisted
# importing required modules
from pypdf import PdfReader

# creating a pdf reader object
reader = PdfReader(r"media/resumes/Yousef_Mohamed_A__Azeem_Sedik.pdf")

# printing number of pages in pdf file
print(len(reader.pages))

# getting a specific page from the pdf file
page = reader.pages[0]

# extracting text from page
text = page.extract_text()
print(text)
