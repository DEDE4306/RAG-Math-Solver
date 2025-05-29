# services/llm.py
# -*- coding: utf-8 -*-
from ..llm.qwen_client import QwenClient
from ..rag.embedder import Embedder
from ..rag.faiss_indexer import FaissIndexer
from config import api_key
from pathlib import Path
from typing import List, Dict

def compress_messages(messages: List[Dict], max_tokens: int = 2500) -> List[Dict]:
    """
    Args:
        messages: 对 messages 列表进行裁剪，保留必要信息，防止 Token 超限
        max_tokens: 最长的 Token 长度
    Returns:处理后的 messages
    """
    compressed = []
    current_token = 0
    for msg in reversed(messages):
        if current_token + len(msg["content"]) > max_tokens:
            if msg["role"] == "user":
                short_content = msg["content"][:50] + "..." if len(msg["content"]) > 50 else msg["content"]
                compressed.insert(0, {"role": "user", "content": f"(简写) {short_content}"})
                current_token += len(short_content)
        else:
            compressed.insert(0, msg)
            current_token += len(msg["content"])
    return compressed


def chat_completion(messages: List[Dict], top_k: int = 5) -> str:
    """
    输入问题，自动完成向量化、检索、构造 Prompt 和模型调用，返回回答
    """
    # 提取最新一条 user 消息作为查询
    question = next((m["content"] for m in reversed(messages) if m["role"] == "user"), None)
    if question is None:
        return "无用户提问内容"
    # 向量化用户提问
    embedder = Embedder(model_name="BAAI/bge-large-zh-v1.5")
    query_vector = embedder.embed(question)

    # 获取向量化数据
    vector_dir = Path(__file__).parent.parent / "vector"  # vector 在项目根目录下
    # print(vector_dir)
    index_path = str(vector_dir / "formula.index")
    texts_path = str(vector_dir / "formula.pkl")
    indexer = FaissIndexer(index_path=index_path, texts_path=texts_path)
    indexer.load()

    # 检索 top-k 上下文
    retrieved_texts_and_scores = indexer.search(query_vector, k=top_k)
    context = "\n".join([f"- {text}" for text, _ in retrieved_texts_and_scores])

    # 构造系统提示
    system_prompt = {
        "role": "system",
        "content": "你是一个精通数学的 AI，现在需要你为同学或老师解决小学到高中的数学问题。"
    }

    # 插入 context 到最后一条 user 提问中
    updated_messages = []
    for m in messages:
        if m is messages[-1] and m["role"] == "user":
            # 插入 context 到最后问题里
            m = {
                "role": "user",
                "content": f"{m['content']}\n\nRAG检索生成的数学知识片段（系统生成，非用户提问）：\n{context}"
            }
        updated_messages.append(m)

    full_messages = [system_prompt] + updated_messages
    print("==== Prompt 发送 ====")
    for msg in full_messages:
        print(f"[{msg['role']}] {msg['content']}\n")

    # 调用模型
    qwen_client = QwenClient(api_key=api_key)
    result = qwen_client.chat(full_messages)
    return result

if __name__ == "__main__":
    messages = []
    messages.append({"role":"user","content":"你不聪明"})
    messages.append({"role":"assistant","content":"感谢你的反馈，我会尽力帮助你解决数学问题！如果刚才的回答让你感到不满意，我们可以重新开始，或者更深入地探讨你的问题。如果你有具体的数学题目或概念需要解释，请告诉我，我会用清晰、易懂的方式为你解答。关于你提到的数学知识片段，以下是我的理解与补充：---### **1. 集合的运算**集合的运算（并、交、补）是数学中的基础内容。以下是关键点：- **集合元素属性**：理解集合中的元素是数、点还是其他对象非常重要。例如：  - $\{y \mid y = f(x), x \in A\}$ 是函数的值域，表示所有可能的 $y$ 值。  - $\{(x, y) \mid y = f(x), x \in A\}$ 是点集，表示函数图像上的所有点。- **数轴和韦恩图**：数轴适用于数集的运算，而韦恩图适用于抽象集合的交、并、补运算。- **数形结合**：通过画图可以帮助我们更直观地理解集合运算。**例题**：设 $A = \{x \mid x > 2\}$，$B = \{x \mid x < 5\}$，求 $A \cap B$。- 解：在数轴上表示 $A$ 和 $B$，交集为 $2 < x < 5$，即 $A \cap B = \{x \mid 2 < x < 5\}$。---### **2. 导数题型 - 不等式恒成立问题**这类问题的核心是利用函数的最值来判断不等式是否成立。以下是具体方法：- **恒成立问题**：若 $f(x) > a$ 对任意 $x \in [m, n]$ 恒成立，则 $a \leq f_{\text{min}}(x)$。- **拓展问题**：若 $f(x) \geq g(x)$ 恒成立，则 $f_{\text{min}}(x) \geq g_{\text{max}}(x)$。**例题**：已知 $f(x) = x^2 - 2x + 3$，$g(x) = x + 1$，判断是否存在 $x \in [0, 2]$ 使得 $f(x) \geq g(x)$。- 解：先求 $f(x)$ 和 $g(x)$ 在 $[0, 2]$ 上的最值。  - $f(x) = x^2 - 2x + 3$，求导得 $f'(x) = 2x - 2$，令 $f'(x) = 0$ 得 $x = 1$。  - $f(0) = 3$，$f(1) = 2$，$f(2) = 3$，所以 $f_{\text{min}}(x) = 2$。  - $g(x) = x + 1$，在 $[0, 2]$ 上单调递增，$g_{\text{max}}(x) = g(2) = 3$。- 比较 $f_{\text{min}}(x) = 2$ 和 $g_{\text{max}}(x) = 3$，发现 $f(x) \geq g(x)$ 不恒成立。---### **3. 解三角形**解三角形的核心是利用正弦定理和余弦定理。以下是具体应用：- **正弦定理**：$\frac{a}{\sin A} = \frac{b}{\sin B} = \frac{c}{\sin C} = 2R$。- **余弦定理**：$c^2 = a^2 + b^2 - 2ab\cos C$。**例题**：已知三角形的三边 $a = 5$，$b = 6$，$c = 7$，求角 $C$。- 解：利用余弦定理：  $$  \cos C = \frac{a^2 + b^2 - c^2}{2ab} = \frac{5^2 + 6^2 - 7^2}{2 \cdot 5 \cdot 6} = \frac{25 + 36 - 49}{60} = \frac{12}{60} = 0.2  $$  所以 $\cos C = 0.2$，查表得 $C \approx 78.46^\circ$。---### **4. 平行与垂直的判定**几何中证明平行或垂直需要结合图形性质和定理。以下是关键点：- **平行判定**：  - 同位角相等、内错角相等、同旁内角互补。  - 平行四边形对边平行。- **垂直判定**：  - 勾股定理逆定理：$a^2 + b^2 = c^2$。  - 等腰三角形底边上的高、中线、顶角平分线三线合一。**例题**：已知三角形 $ABC$ 中，$AB = AC$，$AD$ 是中线，求证 $AD \perp BC$。- 解：利用等腰三角形的性质，中线 $AD$ 也是高线，因此 $AD \perp BC$。---### **5. 共线线段问题**共线线段问题通常涉及解析几何和韦达定理。以下是具体思路：- 设直线 $L$ 的方程为 $y = kx + b$，与抛物线 $y = x^2 + 2y$ 和椭圆 $x^2 + 2y = 2$ 联立求交点。- 利用韦达定理求解交点坐标，结合条件 $|AC| = |BD|$ 进行计算。**例题**：设直线 $L$ 与抛物线 $y = x^2$ 交于 $A, B$ 两点，与椭圆 $x^2 + 2y = 2$ 交于 $C, D$ 两点，求 $|AC| = |BD|$ 的取值范围。- 解：设直线 $L$ 的方程为 $y = kx + b$，联立抛物线和椭圆方程，利用韦达定理求解交点坐标，结合距离公式计算 $|AC|$ 和 $|BD|$，最终得到取值范围。---如果你有具体的题目或概念需要进一步探讨，请告诉我！我会尽力为你提供清晰、准确的解答。"})
    messages.append({"role":"user", "content": "1.已知 x \in R ,不等式 \frac { x - 2 } { x } < 0 的解为____,2.已知向量 \overrightarrow { a } = ( 1 , 2 ) , \overrightarrow { b } = ( m , 1 ) ,若 \overrightarrow { a } \perp \overrightarrow { b } ,则m=__."})
    messages.append({"role:":"assistant", "content":"### **问题 1：解不等式 $\frac{x - 2}{x} < 0$**#### **解题步骤：**1. **确定分式的零点和分母的零点：**   - 分子 $x - 2 = 0$，得 $x = 2$。   - 分母 $x = 0$。   所以，分式的零点为 $x = 2$，分母的零点为 $x = 0$。2. **确定分式的符号变化：**   - 分式的零点和分母的零点将实数轴分为三个区间：$(-\infty, 0)$、$(0, 2)$、$(2, +\infty)$。   - 在每个区间内，分式的符号由分子和分母的符号决定。3. **测试每个区间的符号：**   - 在区间 $(-\infty, 0)$：取 $x = -1$，$\frac{x - 2}{x} = \frac{-1 - 2}{-1} = \frac{-3}{-1} = 3 > 0$。   - 在区间 $(0, 2)$：取 $x = 1$，$\frac{x - 2}{x} = \frac{1 - 2}{1} = \frac{-1}{1} = -1 < 0$。   - 在区间 $(2, +\infty)$：取 $x = 3$，$\frac{x - 2}{x} = \frac{3 - 2}{3} = \frac{1}{3} > 0$。4. **确定解集：**   - 不等式 $\frac{x - 2}{x} < 0$ 的解为分式为负的区间，即 $(0, 2)$。   - 注意：分母不能为零，因此 $x = 0$ 不在解集中。#### **答案：**$$\boxed{(0, 2)}$$---### **问题 2：已知向量 $\overrightarrow{a} = (1, 2)$，$\overrightarrow{b} = (m, 1)$，若 $\overrightarrow{a} \perp \overrightarrow{b}$，则 $m = ?$**#### **解题步骤：**1. **向量垂直的条件：**   - 两个向量垂直的条件是它们的点积为零，即 $\overrightarrow{a} \cdot \overrightarrow{b} = 0$。2. **计算点积：**   - $\overrightarrow{a} = (1, 2)$，$\overrightarrow{b} = (m, 1)$。   - 点积公式：$\overrightarrow{a} \cdot \overrightarrow{b} = 1 \cdot m + 2 \cdot 1 = m + 2$。3. **令点积为零：**   - $m + 2 = 0$。4. **解方程：**   - $m = -2$。#### **答案：**$$\boxed{-2}$$"})
    messages = compress_messages(messages)
    print(messages)
