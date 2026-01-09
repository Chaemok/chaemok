<template>
  <footer class="bg-slate-950 text-slate-300 font-pretendard pt-16 pb-8 border-t border-slate-900">
    <div class="max-w-7xl mx-auto px-6">
      
      <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-12 mb-16">
        
        <div class="space-y-6">
          <div class="flex items-center gap-2 group cursor-default">
            <span class="text-3xl transition-transform group-hover:scale-110 duration-500">🐜</span>
            <span class="text-2xl font-black tracking-tighter text-white">
              Smart <span class="text-blue-500">Ants</span>
            </span>
          </div>
          <p class="text-sm text-slate-400 leading-relaxed font-medium">
            데이터 및 AI기반으로 금융 정보를 한 눈에.<br>
            주식, 예/적금 추천 서비스.
          </p>
          <div class="flex gap-4 pt-2">
            <div class="w-8 h-8 rounded-full bg-slate-800 flex items-center justify-center hover:bg-blue-600 transition-colors cursor-pointer text-white">N</div>
            <div class="w-8 h-8 rounded-full bg-slate-800 flex items-center justify-center hover:bg-black transition-colors cursor-pointer text-white">G</div>
          </div>
        </div>

        <div>
          <h4 class="text-white font-bold mb-6">Service</h4>
          <ul class="space-y-3 text-sm font-medium">
            <li><router-link to="/news" class="hover:text-blue-400 transition-colors">금융 뉴스</router-link></li>
            <li><router-link to="/youtube" class="hover:text-blue-400 transition-colors">금융 Youtube</router-link></li>
            <li><router-link to="/deposit" class="hover:text-blue-400 transition-colors">예/적금 비교</router-link></li>
            <li><router-link to="/stocks" class="hover:text-blue-400 transition-colors">주식 종목 추천</router-link></li>
            <li><router-link to="/market" class="hover:text-blue-400 transition-colors">주식 시장 대시보드</router-link></li>
            <li><router-link to="/market/exchange-rate" class="hover:text-blue-400 transition-colors">환율 정보</router-link></li>
            <li><router-link to="/market/commodity" class="hover:text-blue-400 transition-colors">금/은 정보</router-link></li>
            <li><router-link to="/map" class="hover:text-blue-400 transition-colors">은행/증권사 찾기</router-link></li>
          </ul>
        </div>

        <div>
          <h4 class="text-white font-bold mb-6">Community</h4>
          <ul class="space-y-3 text-sm font-medium">
            <li><router-link to="/community?category=free" class="hover:text-blue-400 transition-colors">자유게시판</router-link></li>
            <li><router-link to="/community?category=qna" class="hover:text-blue-400 transition-colors">Q&A</router-link></li>
            <li><router-link to="/community?category=review" class="hover:text-blue-400 transition-colors">상품후기</router-link></li>
            <li><router-link to="/community?category=tips" class="hover:text-blue-400 transition-colors">투자 꿀팁</router-link></li>
            <li><router-link to="/community?category=faq" class="hover:text-blue-400 transition-colors">FAQ</router-link></li>
            <li><router-link to="/community?category=inquiry" class="hover:text-blue-400 transition-colors">1:1문의</router-link></li>
          </ul>
        </div>

        <div>
          <h4 class="text-white font-bold mb-6">Project Info</h4>
          <div class="text-xs text-slate-500 space-y-3 leading-relaxed">
            <p>
              <span class="text-slate-400 font-bold block mb-1">SSAFY 14th Financial Capstone</span>
              본 서비스는 삼성청년SW아카데미(SSAFY) 교육 과정의 일환으로 제작된 학습용 프로젝트입니다.
            </p>
            <p class="pt-2 border-t border-slate-900/50">
              실제 금융 거래 기능은 제공되지 않으며,<br> 
              상업적 목적으로 사용되지 않습니다.
            </p>
          </div>
        </div>
      </div>

      <div class="pt-8 border-t border-slate-900 flex flex-col md:flex-row justify-between items-center gap-4 text-xs font-medium text-slate-500">
        <p>Copyright © 2025 Lee Chae-Mok & Go Ji-Hun. All rights reserved.</p>
        <div class="flex gap-6">
          <span class="hover:text-slate-300 cursor-pointer">이용약관</span>
          <span class="hover:text-slate-300 cursor-pointer">개인정보처리방침</span>
        </div>
      </div>
    </div>
  </footer>
</template>