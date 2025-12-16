# trip_planner
基于langchain1.1版本和高德mcp server的多智能体agent旅游助手

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

## 项目预览（文字描述）

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
<img width="607" height="301" alt="image" src="https://github.com/user-attachments/assets/9e328930-5f4b-402c-8906-dab04b3af461" />
