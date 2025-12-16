import json
from schemas import TripRequest, TripPlan
from trip_planner.my_llm import llm1
from trip_planner.env_utils import *
from langchain_mcp_adapters.client import MultiServerMCPClient
from langchain.agents import create_agent
import asyncio
from prompts import *

class MultiAgentTripPlanner:
    """多智能体旅行规划系统"""

    def __init__(self):
        self.llm = llm1
        self.amap_tool = None
        self.weather_agent = None
        self.attraction_agent = None
        self.hotel_agent = None
        self.planner_agent = None

    async def initialize(self):
        """初始化多智能系统"""
        print("初始化多智能体旅行规划系统...")
        try:
            print("  - 创建共享MCP工具...")
            self.amap_tool = MultiServerMCPClient(
                {
                    "amap-amap-sse": {
                      "url": "https://mcp.amap.com/sse?key={}".format(AMAP_API_KEY),
                      "transport": "sse",
                  }  
                }
            )
            tools = await self.amap_tool.get_tools()

            print("  - 创建天气查询Agent...")
            self.weather_agent = create_agent(
                self.llm,
                tools,
                system_prompt=WEATHER_AGENT_PROMPT
            )

            print("  - 创建景点搜索Agent...")
            self.attraction_agent = create_agent(
                self.llm,
                tools,
                system_prompt=ATTRACTION_AGENT_PROMPT
            )

            print("  - 创建酒店推荐Agent...")
            self.hotel_agent = create_agent(
                llm1,
                tools,
                system_prompt=HOTEL_AGENT_PROMPT
            )

            print("  - 创建行程规划Agent...")
            self.planner_agent = create_agent(
                self.llm,
                system_prompt=PLANNER_AGENT_PROMPT
            )

            print(f"✅ 多智能体系统初始化成功")
            # 正确打印共享工具数量
            print(f"   共享高德地图工具数量: {len(tools)} 个")
            # 可选：列出工具名称，便于调试
            print(f"   可用工具: {[tool.name for tool in tools]}")

        except Exception as e:
            print(f"❌ 多智能体系统初始化失败: {str(e)}")
            import traceback
            traceback.print_exc()
            raise
        
    async def plan_trip(self, request: TripRequest) -> TripPlan:
        """
        使用多智能体进行旅行规划
        
        Args:
            request: 旅行请求
            
        Returns:
            旅行计划
        """
        try:
            print(f"\n{'='*60}")
            print(f"🚀 开始多智能体协作规划旅行...")
            print(f"目的地: {request.city}")
            print(f"日期: {request.start_date} 至 {request.end_date}")
            print(f"天数: {request.travel_days}天")
            print(f"偏好: {', '.join(request.preferences) if request.preferences else '无'}")
            print(f"{'='*60}\n")

            print("📍 步骤1: 搜索景点...")
            attraction_query = self._build_attraction_query(request)
            attraction_response =await self.attraction_agent.ainvoke(attraction_query)
            attraction_text = self._extract_text(attraction_response)
            print(f"景点搜索结果: {attraction_text[:200]}...\n")

            await asyncio.sleep(1)

            print("🌤️  步骤2: 查询天气...")
            weather_query = {
                "messages": [("user", f"请查询{request.city}从{request.start_date}到{request.end_date}的天气预报，包括每天白天/夜间温度和天气状况。")]
                }
            weather_response = await self.weather_agent.ainvoke(weather_query)
            weather_text = self._extract_text(weather_response)
            print(f"天气查询结果: {weather_text[:200]}...\n")

            await asyncio.sleep(1)

            print("🏨 步骤3: 搜索酒店...")
            hotel_query = {
                "messages": [("user", f"请在{request.city}搜索{request.accommodation}，推荐6-10家位置方便、价格适中的酒店，包括名称、地址、大致价格、评分等信息。")]
                }
            hotel_response = await self.hotel_agent.ainvoke(hotel_query)
            hotel_text = self._extract_text(hotel_response)
            print(f"酒店搜索结果: {hotel_text[:200]}...\n")

            await asyncio.sleep(1)

            print("📋 步骤4: 生成行程计划...")
            planner_query = self._build_planner_query(request, attraction_text, weather_text, hotel_text)
            planner_input = {"messages": [("user", planner_query)]}
            planner_response = await self.planner_agent.ainvoke(planner_input)
            planner_text = self._extract_text(planner_response)
            print(f"行程规划结果: {planner_text[:800]}...\n")

            trip_plan = self._parse_response(planner_text,request)

            print(f"{'='*60}")
            print(f"✅ 旅行计划生成完成!")
            print(f"{'='*60}\n")

            return trip_plan

        except Exception as e:
            print(f"❌ 旅行规划失败: {str(e)}")
            import traceback
            traceback.print_exc()
            raise
      
    def _build_attraction_query(self, request: TripRequest) -> dict:
        """构建景点搜索查询"""
        preferences = ', '.join(request.preferences) if request.preferences else "经典景点"
        return {
        "messages": [
            ("user", f"请搜索{request.city}适合{request.travel_days}天游玩的{preferences}，推荐8-12个热门景点，包括名称、地址、简介、门票价格等信息。")
        ]
    }

    def _build_planner_query(self, request: TripRequest, attractions: str, weather: str, hotels: str = "") -> dict:
        """构建行程规划查询"""
        query = f"""请根据以下信息生成{request.city}的{request.travel_days}天旅行计划:

**基本信息:**
- 城市: {request.city}
- 日期: {request.start_date} 至 {request.end_date}
- 天数: {request.travel_days}天
- 交通方式: {request.transportation}
- 住宿: {request.accommodation}
- 偏好: {', '.join(request.preferences) if request.preferences else '无'}

**景点信息:**
{attractions}

**天气信息:**
{weather}

**酒店信息:**
{hotels}

**要求:**
1. 每天安排2-3个景点
2. 每天必须包含早中晚三餐
3. 每天推荐一个具体的酒店(从酒店信息中选择)
3. 考虑景点之间的距离和交通方式
4. 返回完整的JSON格式数据
5. 景点的经纬度坐标要真实准确
"""
        if request.free_text_input:
            query += f"\n**额外要求:** {request.free_text_input}"

        return query

    def _parse_response(self, response: str, request: TripRequest) -> TripPlan:
        """
        解析Agent响应
        
        Args:
            response: Agent响应文本
            request: 原始请求
            
        Returns:
            旅行计划
        """
        try:
            # 尝试从响应中提取JSON
            # 查找JSON代码块
            if "```json" in response:
                json_str = response.split("```json")[1].split("```")[0].strip()
            elif "```" in response:
                parts = response.split("```")
                if len(parts) >= 3:
                    json_str = parts[1].strip()
                else:
                    json_str = parts[-1].strip()
            else:
                start = response.rfind("{")
                if start == -1:
                    raise ValueError("未找到 {")
                # 从 start 开始向后找匹配的 }
                bracket_count = 0
                end = start
                for i, char in enumerate(response[start:], start):
                    if char == '{':
                        bracket_count += 1
                    elif char == '}':
                        bracket_count -= 1
                        if bracket_count == 0:
                            end = i + 1
                            break
                if bracket_count != 0:
                    raise ValueError("JSON 大括号不匹配")
                json_str = response[start:end]
            
            # 解析JSON
            json_str = json_str.strip()
            print(f"提取到的JSON:\n{json_str[:500]}...")

            data = json.loads(json_str)
            
            # 转换为TripPlan对象
            trip_plan = TripPlan(**data)
            
            return trip_plan
        
        except json.JSONDecodeError as e:
            print(f"JSON 解析错误: {e}")
            print(f"问题JSON内容:\n{json_str[:1000]}")
            raise
        except Exception as e:
            print(f"提取JSON失败: {e}")
            print(f"原始响应:\n{response[:1000]}")
            raise

    def _extract_text(self, response) -> str:
      """从 Agent 响应中提取可读的文本内容"""
      if isinstance(response, str):
          return response
      elif isinstance(response, dict):
          # 最常见的情况：{"messages": [..., AIMessage(content="...")]}
          if "messages" in response:
              messages = response["messages"]
              if messages:
                  last_msg = messages[-1]
                  if hasattr(last_msg, "content"):
                      content = last_msg.content
                      if isinstance(content, str):
                          return content
                      elif isinstance(content, list):  # 有时是 content blocks
                          return "".join([c.get("text", "") for c in content if c.get("type") == "text"])
          # 备用：直接 str 整个 dict（调试用）
          return str(response)[:500]
      else:
          return str(response)[:500]
      
_multi_agent_planner = None

def get_trip_planner_agent() -> MultiAgentTripPlanner:
    """获取多智能体系统实例"""
    global _multi_agent_planner
    if _multi_agent_planner is None:
        _multi_agent_planner = MultiAgentTripPlanner()
    return _multi_agent_planner

async def main():
    """主入口函数"""
    planner = MultiAgentTripPlanner()
    await planner.initialize()
    print("✅ 系统初始化成功")
    request = TripRequest(
        city="北京",
        start_date="2025-12-16",
        end_date="2025-12-18",
        travel_days=3,
        transportation="公共公交",
        accommodation="经济型酒店",
        preferences=["历史文化", "美食"],
        free_text_input="多安排博物馆，避免拥挤景点"
    )
    try:
        trip_plan = await planner.plan_trip(request)
        print("\n✅ 生成的旅行计划：")
        print(trip_plan.model_dump_json(indent=2))  # 漂亮打印JSON
    except Exception as e:
        print(f"规划失败: {e}")

if __name__ == "__main__":
    """测试多智能体系统"""
    asyncio.run(main())


