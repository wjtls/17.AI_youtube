# 대사 생성

from dotenv import load_dotenv
# API 키 정보 로드
load_dotenv(override=True)


from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.prompts import ChatPromptTemplate,PromptTemplate
from langchain_core.runnables import RunnablePassthrough, RunnableLambda
from langchain_core.output_parsers import StrOutputParser

import json
import os



def generate_content(save_name,content_type,user_content,country_code): #대본생성
    # AI보고서 호출
    with open("../b_finance_RAG_AI/traj/report_chat_history.json", "r") as file:
        data = json.load(file)

    finance_context =data[-1].get('응답')

    content_llm = ChatGoogleGenerativeAI(model="gemini-2.0-flash",
                                                   temperature= 0.1,
                                                   max_output_tokens=8192,
                                                   api_key=os.environ["GOOGLE_API_KEY"])  # 노드에서 사용되는 gpt(요약,웹서치 키워드생성,판단 등)


    if country_code == 'ko':
        country='한국어'
        자막 ='영어'
    if country_code == 'en':
        country='영어'
        자막 = '한국어'
    if country_code == 'ja':
        country='일본어'
        자막 = '한국어'

    if content_type =='news':
        prompt="""
##너는 유튜브 영상 {country} 대본을 작성하는 AI다. {country} 언어로 쓰세요
# AI 분석 정보 : 해당내용은 트레이더 AI가 작성한 실시간 금융시장 분석 리포트입니다 
# AI 분석 정보가 들어오면 해당내용으로 90초짜리 동영상 대본을 작성하세요.
# 나래이션에서는 AI가 실시간 분석한 결과임을 암시하세요. 
# 전체적 흐름은 인사 -> 분석대상 -> 뉴스내용 -> 분석 -> AI의 추천 매매 의사결정 -> 마지막인사 입니다
# 나래이션 : 나래이션들은 자연스럽게 이어지도록 모두 {country} 언어로 작성하세요, 전문가가 썼다는 말대신 AI가 분석했다는 말을 쓰세요
# 타이틀 : 모두 {country} 언어로 작성하세요
# 자막 : 자막은 나래이션을 {자막} 언어로 번역하여 쓰세요.
# 장면 : 대본에 장면을 포함하는데 장면은 영어로 매우 자세하고 상세하게 묘사하여 이미지AI모델의 프롬프트로 쓰세요.
        -> 사람들이 계속 봐야하므로 어그로가 잘끌리게 시각적으로 즐겁고, 창의적인 장면들을 생성하세요/ 특정 사람이나 기업이름은 절대 쓰지마세요
        
# 영상 마지막은 인삿말로 결론과 구독,좋아요를 누르고 AI분석 결과를 실시간으로 들을수있다고 홍보하세요

형식은 아래와같습니다 반드시 지키세요.
각 영상 시간대를 나누어 각각의 시간대에 아래와같이 기입하세요 (각 시간대는 7초를 넘기지마세요)
시간대 : 
타이틀 :
장면 : 
나래이션:
자막:
각요소마다 줄바꿈하고 요소 내부에서는 줄바꿈 쓰지마세요 (ex 시간대: ~ 다쓰고나서 줄바꿈)

AI 분석 정보 : {context}
        """
        llm_chain = (
                {'context': RunnablePassthrough(),'country': RunnablePassthrough(),'자막': RunnablePassthrough()}
                | PromptTemplate(template=prompt, input_variables=['context','country','자막'])
                | content_llm
                | StrOutputParser()
        )

        input_data = {'context': str(finance_context),'country':country,'자막':자막}
        res = llm_chain.invoke(input_data)




    if content_type =='fun':
        prompt = """
##너는 유튜브 영상 {country} 대본을 작성하는 AI다.{country} 언어로 쓰세요
# 주제 : 해당내용 당신이 써야할 대본의 주제이다
# 주제가 들어오면 해당내용으로 70~80초짜리 동영상 대본을 처음부터 결말까지 작성하세요. (독자는 20~30대 과학전문가들 입니다)
# 최대한 상상력,깊이있는 과학을 동원하여 논리적으로 쓰고,사람들이 생각지도못하는 참신한이야기로 쓰세요 
# 절대 유치하게쓰지말고,일의 인과관계를 과학적으로 논리적으로 쓰세요.
# 최대한 자극적이고, 불쾌하게끔하고, 과장하여쓰세요, 상황을 자세하게 쓰세요

# 나래이션 : 자연스럽게 이어지도록 {country}로 설명을 쓰세요 (텍스트만 쓰세요)
# 자막 : 자막은 나래이션을 {자막}언어로 번역하여 작성하세요.
# 장면: 장면은 영어로 매우 자세하고 상세하게 묘사하세요
# 장면: 사람들이 계속 봐야하므로 어그로가 잘끌리게 창의적인 장면들을 생성하세요/ 특정 사람이나 기업이름은 절대 쓰지마세요
# 장면: 최대한 자극적(창의)이고, 불쾌(ex메갈로포비아)하게끔하고, 과장(ex목성공포증)하세요
# 영상 마지막은 인삿말로 결론과 구독,좋아요를 누르고 AI가 스스로 만든 영상을 볼수있다고 홍보하세요

형식은 아래와같습니다 반드시 지키세요.
각 영상 시간대를 나누어 각각의 시간대에 아래와같이 기입하세요 (각 시간대는 7초를 넘기지마세요)
시간대 : 
타이틀 :
장면 : 
나래이션:
자막:
각요소마다 줄바꿈하고 요소 내부에서는 줄바꿈 쓰지마세요 (ex 시간대: ~ 다쓰고나서 줄바꿈)

주제 : {context}
                """

        llm_chain = (
                {'context': RunnablePassthrough(), 'country': RunnablePassthrough(), '자막': RunnablePassthrough()}
                | PromptTemplate(template=prompt, input_variables=['context', 'country', '자막'])
                | content_llm
                | StrOutputParser()
        )

        input_data = {'context': user_content,'country':country,'자막':자막}
        res = llm_chain.invoke(input_data)

    if content_type == 'fun-ranking': # 랭킹 쇼츠
        prompt = """
                """

        llm_chain = (
                {'context': RunnablePassthrough(), 'country': RunnablePassthrough(), '자막': RunnablePassthrough()}
                | PromptTemplate(template=prompt, input_variables=['context', 'country', '자막'])
                | content_llm
                | StrOutputParser()
        )

        input_data = {'context': user_content, 'country': country, '자막': 자막}
        res = llm_chain.invoke(input_data)

    #저장
    res_json = {"대본":res,"정보":finance_context}
    with open(f'content_data/{country_code}_{save_name}.json', 'w', encoding='utf-8') as f:
        json.dump(res_json, f, ensure_ascii=False, indent=4)


    print('대본생성에 참고한 보고서:', finance_context)
    print('대본:',res)

    return res,finance_context


if __name__ == "__main__":
    file_name = '테스트_저장_2025-03-27'
    user_content = 'AI가 골렘의 사원에 들어갔다면 ?'
    country_code= 'ko'
    res,finance_context= generate_content(file_name,'news',user_content,country_code)
    print('user_content :',user_content)
    print('대본생성에 참고한 보고서:', finance_context)
    print('대본:',res)