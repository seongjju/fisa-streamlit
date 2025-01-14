import streamlit as st

# text를 입력하는 검색창 하나 만들기
# anly_list에 있는 글자가 일부라도 들어가면 
# 이미지 리스트에 있는 검색창을 하나 만들어주세요

word= st.text_input("검색하실 애니메이션을 입력하세요")
ani_list = ['짱구는못말려', '몬스터','릭앤모티']
img_list = ['https://i.imgur.com/t2ewhfH.png', 
            'https://i.imgur.com/ECROFMC.png', 
            'https://i.imgur.com/MDKQoDc.jpg']
dict={}
for i in range(len(ani_list)):
    dict[ani_list[i]] = img_list[i]

if not word:
    st.text("No title")
else:
    for ani in ani_list:
        if word in ani:
            st.image(dict[ani], width=1000)
    
#     print(ani)
# print(word)
