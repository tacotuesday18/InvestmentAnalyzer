import os
import streamlit as st
from typing import Optional

# API Configuration and Management
class APIConfig:
    """
    API設定と管理クラス
    """
    
    def __init__(self):
        self.gemini_api_key = None
        self.openai_api_key = None
        self.load_api_keys()
    
    def load_api_keys(self):
        """
        環境変数またはStreamlit secretsからAPIキーを読み込む
        """
        # Gemini API Key
        self.gemini_api_key = (
            os.environ.get("GEMINI_API_KEY") or 
            st.secrets.get("GEMINI_API_KEY") if hasattr(st, 'secrets') and 'GEMINI_API_KEY' in st.secrets else None
        )
        
        # OpenAI API Key
        self.openai_api_key = (
            os.environ.get("OPENAI_API_KEY") or 
            st.secrets.get("OPENAI_API_KEY") if hasattr(st, 'secrets') and 'OPENAI_API_KEY' in st.secrets else None
        )
    
    def has_gemini_key(self) -> bool:
        """Gemini APIキーが設定されているか確認"""
        return self.gemini_api_key is not None and self.gemini_api_key != ""
    
    def has_openai_key(self) -> bool:
        """OpenAI APIキーが設定されているか確認"""
        return self.openai_api_key is not None and self.openai_api_key != ""
    
    def get_gemini_client(self):
        """
        Gemini APIクライアントを取得
        """
        if not self.has_gemini_key():
            st.error("⚠️ Gemini APIキーが設定されていません")
            st.info("環境変数 `GEMINI_API_KEY` を設定してください")
            return None
        
        try:
            import google.generativeai as genai
            genai.configure(api_key=self.gemini_api_key)
            return genai
        except ImportError:
            st.error("google-generativeai パッケージがインストールされていません")
            st.code("pip install google-generativeai", language="bash")
            return None
        except Exception as e:
            st.error(f"Gemini API初期化エラー: {str(e)}")
            return None
    
    def get_openai_client(self):
        """
        OpenAI APIクライアントを取得
        """
        if not self.has_openai_key():
            st.error("⚠️ OpenAI APIキーが設定されていません")
            st.info("環境変数 `OPENAI_API_KEY` を設定してください")
            return None
        
        try:
            from openai import OpenAI
            client = OpenAI(api_key=self.openai_api_key)
            return client
        except ImportError:
            st.error("openai パッケージがインストールされていません")
            st.code("pip install openai", language="bash")
            return None
        except Exception as e:
            st.error(f"OpenAI API初期化エラー: {str(e)}")
            return None
    
    def test_gemini_connection(self) -> bool:
        """
        Gemini API接続をテスト
        """
        genai = self.get_gemini_client()
        if not genai:
            return False
        
        try:
            model = genai.GenerativeModel('gemini-pro')
            response = model.generate_content("Hello")
            return True
        except Exception as e:
            st.error(f"Gemini接続テスト失敗: {str(e)}")
            return False
    
    def test_openai_connection(self) -> bool:
        """
        OpenAI API接続をテスト
        """
        client = self.get_openai_client()
        if not client:
            return False
        
        try:
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": "Hello"}],
                max_tokens=5
            )
            return True
        except Exception as e:
            st.error(f"OpenAI接続テスト失敗: {str(e)}")
            return False
    
    def display_api_status(self):
        """
        API接続状態を表示
        """
        st.markdown("### 🔌 API接続状態")
        
        col1, col2 = st.columns(2)
        
        with col1:
            if self.has_gemini_key():
                st.success("✅ Gemini API: 接続済み")
            else:
                st.error("❌ Gemini API: 未設定")
        
        with col2:
            if self.has_openai_key():
                st.success("✅ OpenAI API: 接続済み")
            else:
                st.error("❌ OpenAI API: 未設定")
        
        # テストボタン
        if st.button("🔍 API接続をテスト"):
            with st.spinner("テスト中..."):
                col_a, col_b = st.columns(2)
                
                with col_a:
                    if self.has_gemini_key():
                        if self.test_gemini_connection():
                            st.success("Gemini: 接続成功")
                        else:
                            st.error("Gemini: 接続失敗")
                
                with col_b:
                    if self.has_openai_key():
                        if self.test_openai_connection():
                            st.success("OpenAI: 接続成功")
                        else:
                            st.error("OpenAI: 接続失敗")
    
    def setup_api_keys_ui(self):
        """
        APIキー設定UI（開発用）
        """
        st.markdown("### 🔑 APIキー設定")
        st.warning("⚠️ 本番環境では環境変数を使用してください")
        
        with st.form("api_setup_form"):
            gemini_key = st.text_input(
                "Gemini API Key",
                value=self.gemini_api_key or "",
                type="password",
                help="https://makersuite.google.com/app/apikey から取得"
            )
            
            openai_key = st.text_input(
                "OpenAI API Key",
                value=self.openai_api_key or "",
                type="password",
                help="https://platform.openai.com/api-keys から取得"
            )
            
            if st.form_submit_button("保存", use_container_width=True):
                if gemini_key:
                    os.environ["GEMINI_API_KEY"] = gemini_key
                    self.gemini_api_key = gemini_key
                
                if openai_key:
                    os.environ["OPENAI_API_KEY"] = openai_key
                    self.openai_api_key = openai_key
                
                st.success("APIキーを保存しました！")
                st.rerun()


# Gemini API Helper Functions
def analyze_with_gemini(prompt: str, api_config: APIConfig) -> Optional[str]:
    """
    Gemini APIで分析を実行
    
    Parameters:
    -----------
    prompt : str
        分析プロンプト
    api_config : APIConfig
        API設定オブジェクト
        
    Returns:
    --------
    Optional[str]
        分析結果テキスト
    """
    genai = api_config.get_gemini_client()
    if not genai:
        return None
    
    try:
        model = genai.GenerativeModel('gemini-pro')
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        st.error(f"Gemini分析エラー: {str(e)}")
        return None


# OpenAI API Helper Functions
def analyze_with_openai(prompt: str, api_config: APIConfig, model: str = "gpt-4") -> Optional[str]:
    """
    OpenAI APIで分析を実行
    
    Parameters:
    -----------
    prompt : str
        分析プロンプト
    api_config : APIConfig
        API設定オブジェクト
    model : str
        使用するモデル (gpt-4, gpt-3.5-turbo, etc.)
        
    Returns:
    --------
    Optional[str]
        分析結果テキスト
    """
    client = api_config.get_openai_client()
    if not client:
        return None
    
    try:
        response = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": "あなたは金融アナリストです。企業分析のエキスパートとして、詳細な分析を提供してください。"},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=2000
        )
        return response.choices[0].message.content
    except Exception as e:
        st.error(f"OpenAI分析エラー: {str(e)}")
        return None


# グローバルインスタンス
api_config = APIConfig()


# 使用例
if __name__ == "__main__":
    st.title("API設定テスト")
    
    config = APIConfig()
    
    # API状態表示
    config.display_api_status()
    
    st.markdown("---")
    
    # APIキー設定UI
    config.setup_api_keys_ui()
    
    st.markdown("---")
    
    # テスト分析
    if st.button("テスト分析を実行"):
        test_prompt = "Appleの2023年の業績について簡単に分析してください。"
        
        st.markdown("### Gemini分析結果")
        gemini_result = analyze_with_gemini(test_prompt, config)
        if gemini_result:
            st.write(gemini_result)
        
        st.markdown("### OpenAI分析結果")
        openai_result = analyze_with_openai(test_prompt, config, model="gpt-3.5-turbo")
        if openai_result:
            st.write(openai_result)
