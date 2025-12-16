# AI_Trip_Planner
基于langchain1.1版本和高德mcp server的多智能体agent旅游助手

这是一个入门级的agent项目，非常适合新手来了解agent和mcp的原理及应用，并且代码非常简洁，对于刚入门的新手很友好

# AI旅行助手（AI Trip Planner）

一个基于 **LangChain + FastAPI + 高德地图API** 的智能旅行行程规划系统。

用户只需在网页中输入目的地、旅行日期、交通方式、住宿偏好等信息，系统会自动调用大语言模型（DeepSeek）和高德地图工具，实时搜索景点、天气、酒店，并生成详细、可执行的**多天旅行计划**，包括每日行程、餐饮推荐、酒店建议、天气预报和预算估算。

## 功能亮点

- 多智能体（Multi-Agent）协作架构：景点搜索、天气查询、酒店推荐、行程规划四个专用 Agent 分工协作
- 真实数据来源：所有景点、酒店、天气信息均来自高德地图 API，绝不编造
- 详细行程输出：每日 2-3 个景点 + 早中晚三餐 + 具体酒店推荐 + 门票/餐饮/住宿费用估算
- 包含天气预报、总体建议和完整预算表
- 前端美观：Tailwind CSS + 响应式设计 + 手风琴式每日行程折叠
- 支持用户自定义偏好和额外要求（如“多安排博物馆”“避免拥挤景点”）

## 项目预览

提交请求后，页面会展示：

- 旅行标题（如“北京 3天旅行计划”）
- 每日天气卡片
- 可折叠的每日详细行程（交通、住宿、具体酒店、景点列表、餐饮推荐）
- 总体旅行建议和预算汇总

## 技术栈

- **后端**: FastAPI + Uvicorn
- **AI框架**: LangChain + LangChain-MCP-Adapters（调用高德地图工具）
- **大模型**: DeepSeek（通过通义千问/DeepSeek API 调用）
- **地图服务**: 高德地图 Web 服务 API（POI搜索 + 天气查询）
- **前端**: HTML + Tailwind CSS CDN + 原生 JavaScript（无构建工具，打开即用）
- **其他**: Pydantic v2、python-dotenv、httpx-sse、sse-starlette

## 项目结构

- .
- ├── trip_planner/
- │   ├── trip_planner_agent.py
- │   ├── schemas.py
- │   ├── prompts.py
- │   ├── index.html
- │   └── main.py
- ├── my_llm.py
- ├── env_utils.py
- ├── requirements.txt
- ├── .env
- └── README.md

| 文件/目录 | 功能描述 |
| :--- | :--- |
| `trip_planner/` | 存放旅行规划核心逻辑和相关组件的目录。 |
| `trip_planner/trip_planner_agent.py` | 实现了整个应用框架的多智能体核心逻辑。 |
| `trip_planner/schemas.py` | 使用 Pydantic 定义所有输入、输出和内部数据的数据格式。 |
| `trip_planner/prompts.py` | 集中管理和配置系统中各个 Agent 的系统提示词（System Prompts）。 |
| `trip_planner/index.html` | 项目的前端页面文件。 |
| `trip_planner/main.py` | 基于 FastAPI 框架构建的 API 主入口文件。 |
| `my_llm.py` | 用于配置和初始化大型语言模型 (LLM) 访问参数。 |
| `env_utils.py` | 环境变量加载工具，负责读取和处理项目配置。 |
| `requirements.txt` | Python 项目所需的依赖库列表。 |
| `.env` | 环境变量模板文件。**重要：** 使用前需要复制并根据实际环境填写配置。 |
| `README.md` | 项目说明文档（当前文件）。 |

## 快速开始

- 创建并激活虚拟环境（推荐）
  conda create -n trip_planner python==3.11
  conda activate trip_planner
  
- 安装依赖
  pip install -r requirements.txt

- 配置环境变量
  在.env文件里配置自己的APIKey:
    - 高德地图 Key 申请地址：https://lbs.amap.com/api/webservice/guide/api/key
    - 通义千问 API：https://help.aliyun.com/zh/dashscope/

- 启动后端
  python main.py 或使用 uvicorn main:app --reload --host 127.0.0.1 --port 8000

- 打开前端
  - 可以下载vscode插件Live Server
  - 或者直接在浏览器打开 index.html 文件，访问http://127.0.0.1:5500
 
- 开始规划旅行！
  填写表单 → 点击“生成行程计划” → 等待几秒即可看到详细计划。
  
