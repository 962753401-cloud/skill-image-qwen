# Qwen-Image-3.0 官方最佳实践案例与完整提示词手册

> 来源：阿里云百炼官方公众号《Qwen Image 3.0 API 正式上线：不只是在追求好看，更在追求好用》（2026-08-05）
> 用途：作为图像生成提示词（Prompt）写作参考，供其他大模型学习官方提示词的结构与写法。

---

## 一、模型概览

Qwen-Image-3.0 已上线阿里云百炼，核心追求从「好看」转向「好用」——生成的图要能成为可直接交付的成品。官方用三个「实」概括这一代能力：

| 能力 | 说明 | 关键指标 |
| --- | --- | --- |
| 内容丰实 | 装得下一整页：试卷、报纸、图鉴、信息图一次生成 | 指令长度提升至 4.5k token |
| 细节真实 | 经得起放大：纹理质感逼近真实材质 | 10px 小字清晰可辨，毛孔发丝纤毫毕现 |
| 知识厚实 | 什么都懂：跨语言、跨领域 | 覆盖 12 国语言、100+ 艺术风格与多种 UI 界面 |

## 二、官方使用技巧（3 条）

1. **指令可以「长」**：4.5k token 是留给复杂版面的——想要九宫格、整版报纸、完整图鉴，就把每个区域、每段文字、每个相对位置都描述清楚，模型接得住。
2. **小字要「点名」**：想要试卷、笔记、论文里的精确文字，直接把要渲染的正文写进指令，模型会照着排。
3. **风格要「说全」**：100+ 艺术风格 + 12 国语言，越具体越准——摄影风写光线镜头氛围，插画风写材质配色笔触。

## 三、提示词结构范式（从 12 个官方案例归纳）

供大模型仿写的通用骨架：

1. **开篇定调**：一句话说明画面类型、画幅方向、整体风格与氛围。例：「这是一张竖版……海报，整体背景为……」
2. **空间动线**：严格按空间顺序（从上到下、从左到右、从主体到背景）逐区域描述，并写明各元素的相对位置关系。
3. **文字逐字写入**：所有需要渲染的文字——标题、正文、标注、价格、页脚——用引号逐字写进提示词，一字不漏。
4. **细节五要素**：色彩给具体色名、材质给质感词、光影给方向与软硬、字体给风格、构图给层次。
5. **收尾约束**：部分案例以「避免……」列出负面约束（乱码、错位、畸变、过曝、水印等），可有效防翻车。
6. **画幅与摄影参数**：写实/人像类可附画幅比例、镜头焦段、光圈等参数（如「竖版 3:4，85mm，f/2」）。

## 四、最佳实践案例与完整提示词（共 12 个）

### 案例 1｜全国统一考试语文试卷（扫描级排版）

- **分类**：能力演示 · 内容丰实
- **生成方式**：文生图
- **提示词语言**：中文
- **能力看点**：整版 A4 试卷排版：密级标识、标题层级、注意事项、阅读材料正文、灰度柱状图、数据来源、页脚，全部文字精确渲染。

**完整提示词**：

```text
这是一张竖版白底黑字的中文考试试卷扫描页，整体呈现 A4 纸张的 flat, scan-style 规整排版，页面四周留有较宽的纯白边缘，文字以清晰的黑色宋体风格印刷，墨迹锐利易读。页面顶部左侧印有小号密级文字“绝密★启用前”。页面上方居中位置排列着大号主标题“2027 年普通高等学校招生全国统一考试”，其正下方以更大字号、加粗字体显示科目标题“语文（甲卷）”。标题下方居中印有考试说明“本试卷共 10 页，23 题。全卷满分 150 分。考试用时 150 分钟。”。随后进入正文说明区，左侧对齐的加粗标题为“注意事项：”，其下方按序号整齐排列三条说明文字：“1. 答卷前，考生务必将自己的姓名、准考证号填写在答题卡上。”“2. 回答选择题时，选出每小题答案后，用 2B 铅笔把答题卡上对应题目的答案标号涂黑。如需改动，用橡皮擦干净后，再选涂其他答案标号。回答非选择题时，将答案写在答题卡上。写在本试卷上无效。”“3. 考试结束后，将本试卷和答题卡一并交回。”。注意事项下方是试卷第一大题标题，左对齐加粗显示“一、现代文阅读（35 分）”，其下为小节标题“（一）现代文阅读 I（本题共 5 小题，19 分）”，再下方是题目引导语“阅读下面的文字，完成 1～5 题。”。页面中部左侧以加粗小标题标出“材料一：”，下方为分段排列的现代文阅读材料正文，首段为“生成式人工智能的迅猛发展，正深刻改变人类的知识生产、信息传播和思维方式。作为新一轮科技革命和产业变革的重要驱动力量，人工智能既带来前所未有的机遇，也引发一系列值得深思的问题。”，第二段为“从历史维度看，技术始终是文明演进的关键变量。印刷术的发明推动了知识的广泛传播，互联网的普及重塑了社会的连接方式，而生成式人工智能则有可能在更高层面上影响人类与知识、与世界的关系。它能够高效生成文本、图像、代码，辅助科学研究，优化公共服务，拓展人类认知的边界。然而，技术的力量强大，越需要价值的引领和制度的规范。”，第三段为“面对人工智能时代，我们不仅要关注技术本身的突破，更要思考如何与之相处：如何确保算法的透明与公平，如何防止虚假信息的泛滥，如何守护人的主体性与创造力，如何在效率与伦理之间找到平衡。未来的竞争，不只是技术的竞争，更是治理能力、文化素养和人文精神的竞争。”，第四段为“人工智能不会取代人类，但善于运用人工智能的人可能会取代不善于运用的人。教育、媒体、政府和每一个社会成员，都需要提升数字素养，培养批判性思维，学会与智能工具协作。唯有如此，我们才能在智能时代行稳致远，让技术真正服务于人的自由而全面的发展。”。材料一正文右下方附有来源注释“（摘编自《光明日报》2026 年 12 月 15 日）”。页面下半部分左侧出现加粗小标题“材料二：”，其下方绘制了一幅灰度柱状图，图表约占页面宽度的一半，图表顶部居中标题为“2018—2026 年我国生成式人工智能企业数量变化”。柱状图左侧为纵轴，顶部标注单位“（家）”，纵轴刻度从上到下依次清晰印有“2000”“1500”“1000”“500”“100”“0”，底部横轴依次标注年份“2018”“2019”“2020”“2021”“2022”“2023”“2024”“2025”“2026”。每个年份对应一根竖向矩形柱，柱体为浅灰填充并带有柔和的灰色边界，具体数值标在柱顶上方，分别为“28”“56”“98”“343”“703”“1189”“1546”“1865”“2073”，整体呈现出平稳的逐年增长趋势。图表右侧并列排布一段说明文字：“截至 2026 年底，我国已发布并备案的生成式人工智能服务大模型达 428 个，广泛应用于办公、教育、医疗、工业设计、文化传播等领域，用户规模超过 6.5 亿。与此同时，相关伦理规范、法律法规和行业标准也在不断完善。”。柱状图下方左侧印有数据来源说明“（数据来源：国家互联网信息办公室《生成式人工智能发展报告（2027）》）”。页面底部居中印有页脚文字“语文（甲卷） 第 1 页（共 10 页）”。整页视觉元素由黑白印刷文字、单个灰色柱状统计图、细黑坐标轴和充足的页面留白构成，版式严谨规整，完美呈现正式高考试卷首页的专业文档风格。
```

### 案例 2｜刺绣微距（丝线与针脚）

- **分类**：能力演示 · 细节真实
- **生成方式**：文生图
- **提示词语言**：中文
- **能力看点**：微距写实摄影：织物纹理、绣线光泽、针脚走向、浅景深虚化，放大后质感依然成立。

**完整提示词**：

```text
画面是一张横向构图的写实摄影特写，主体集中在刺绣过程中的双手、绣绷和布面图案。整体背景为柔和的米白与浅灰色调，景深较浅，左上与边缘区域轻微虚化，营造出安静、温暖、手作感强的氛围。画面左侧可见一只浅肤色成人手，手指修长，指甲自然短圆且未见明显彩色甲油，手背和指节纹理清晰，正以拇指和食指轻轻按住布面上的线迹；右下方另一只浅肤色成人手同样以拇指和食指捏着浅绿色绣线，正在牵引线头，形成一个松弛的弧形线圈。两只手之间有一根细金属绣针横向穿过布面附近，针体呈银灰色反光，连接着浅绿色线，表现出正在进行针线刺绣的瞬间。画面中央到右侧是一块绷在圆形木质绣绷上的浅米色亚麻布，布面有明显细密交织的织物纹理，颜色温和自然；绣绷只露出部分弧形边缘，位于左上至左侧边缘，呈浅木色，表面光滑，作为固定布料的圆形框架。布面右上区域绣有一只小鸟，鸟的身体朝右、头部略向左侧前方，采用米白、浅褐、橄榄绿和灰褐色丝线表现羽毛层次；小鸟眼睛为小而深的黑色点状细节，喙短而尖，胸腹部以浅米白线绣出柔软羽状质感，翅膀和背部由密集短针构成，带有细腻的渐变纹理，尾羽向右下延伸并略微下垂。鸟脚以浅绿色线绣出，细长地站在枝条上，与下方植物枝干相连。画面中部至右侧分布着多根刺绣植物枝条，主枝以棕色和浅褐色线条表现，斜向穿过布面，枝上长有许多细小的麦穗状、叶片状绣纹；叶片多为橄榄绿和灰绿色，呈细长椭圆形或羽状，麦穗则以浅米黄、米白和淡褐色短针密集排列，具有立体的颗粒感。左中部靠近双手的位置有几簇较小的植物芽和穗状装饰，线迹方向清晰，与中央交叉的枝条形成层叠关系。下方中央偏左有一片较大的绿色叶片，采用斜向针法填充，边缘略尖，与棕色枝条贴合。右侧靠近小鸟尾部和鸟身周围还有竖向延伸的枝条与麦穗，部分靠近画面边缘被裁切，增强了近距离观察刺绣作品的感觉。整张图像以自然光或柔和漫射光照明，阴影轻浅，色彩低饱和，强调布料、绣线、木质绣绷和皮肤的细腻质感，呈现出手工刺绣创作中的宁静、精致与专注。
```

### 案例 3｜手写数学复习笔记（三色批注）

- **分类**：能力演示 · 细节真实
- **生成方式**：文生图
- **提示词语言**：英文
- **能力看点**：手写体数学笔记：0.5mm 黑色凝胶笔主文、红蓝批注、手绘几何图、公式与箭头批注的多层级版面。

**完整提示词**：

```text
The image is a realistic, slightly angled overhead photograph of a landscape-oriented sheet of clean, off-white notebook paper resting on a wooden desk. The paper exhibits a subtle fibrous texture and soft, natural daylight illumination with gentle shadows along the edges. The page is densely filled with structured mathematical study notes written primarily with a fine 0.5mm black gel pen, producing thin, fine, uniform hairline strokes with slight ink feathering into the paper fibers and small darker ink pools where the nib pauses. The black text is complemented by fine blue and red fineliner annotations, underlines, arrows, and hand-drawn boxes, creating a clear, multi-color hierarchical layout typical of advanced university-level mathematics review notes.
In the top-left region, the main heading is written in bold black handwriting: "主题： 正多边形的对称群 D_n 的阶与递推关系". Immediately following it on the same line, the phrase "（复习归纳）" is written in blue ink and emphasized with a thick blue horizontal underline drawn directly beneath it.
Below the title, the first section of the derivation begins on the left side. The black handwritten text reads line by line: "1. 设 a_n=|D_n|. 由构造递推:", "将正 n 边形加一条边得到正 (n+1) 边形。", "D_{n+1}=⟨D_n,r_n⟩，其中 r_n 为新增边中垂线的反射。", and "且 D_n∩⟨r_n⟩={ e, r_n s_n }（只有恒等与关于该边的反射）。" Below the word "因此", a fractional derivation is expanded. The formula is written with hand-drawn horizontal fraction bars: "a_{n+1}=|D_{n+1}|= |D_n|·|⟨r_n⟩| / |D_n∩⟨r_n⟩| = a_n·2 / 2 = a_n." To the right of this equation, the blue annotation "（阶保持不变）" is added. The section concludes with the black text: "又 D_3≅S_3，a_3=6，故 a_n=6（对所有 n≥3）。"
In the top-right area, occupying about one-fifth of the page width, a black line-art geometric diagram of a regular polygon is drawn. The outer contour is a near-circular polygon with vertices marked by solid black dots and connected by short straight lines. Inside, multiple symmetry line segments radiate from the center to the vertices. The vertices are labeled with small black text: "V_1", "V_2", "V_n", "V_k", and "V_{n-1}", while the center point is labeled "O". A blue vertical dashed line extends downward from vertex "V_1" through "O", with the blue label "r_n" at its bottom end. A blue horizontal dashed line extends to the right from "O". To the right of this diagram, in the large blank space, a prominent red handwritten annotation reads: "核心：通过“加一条边”构造 D_{n+1}，\n利用交的大小得到阶的递推！". The phrase "阶的递推！" is underscored with a red wavy line, and a red arrow points downward from this text toward the lower sections.
In the middle-right area, a hand-drawn blue rectangular tip box contains the blue text: "易错点：不要忽略 D_n∩⟨r_n⟩\n只有两个元素！". A blue arrow originates from the edge of this box and points leftward toward the main page content.
In the lower-center region, the second section begins with black handwriting: "2. 更一般地，考虑正多边形的旋转子群 C_n=⟨ρ⟩，|ρ|=n.", "设 b_n=|C_n|=n，加一条边得到 C_{n+1}=⟨ρ'⟩，其中 (ρ')^{n+1}=e.", and "因此 b_{n+1}=n+1，显然有递推:". Centered below this text is a hand-drawn blue rectangular box containing the blue formula: "b_{n+1}=b_n+1， b_3=3 ⇒ b_n=n."
In the lower-left area, the third section is written in black ink: "3. 对反射的计数：设 c_n 为反射的个数，\n则 c_n=a_n/2=3（n≥3）。", "递推检验：新增一条边带来两条新的反射轴，", and "c_{n+1}=c_n+2，c_3=3 ⇒ c_n=2n-3.". The expression "c_n=2n-3" is emphasized with a blue double underline, and a red arrow points directly to this conclusion. Further down on the left, the fourth section title is written in blue: "4. 小结（待证明的结构事实）：". Below it, a mix of black and blue text lists the points: "(1) D_{n+1}=⟨D_n,r_n⟩， D_n∩⟨r_n⟩={e, r_n s_n}", "(2) |D_{n+1}|=|D_n|， |D_n|=2n（与上面推出的恒等相一致）", and "(3) 递推体系： b_{n+1}=b_n+1，b_n=n；\nc_{n+1}=c_n+2，c_n=2n-3."
In the bottom-right corner, a hand-drawn red rectangular summary box contains the red text: "结论（已归纳）：\n① |D_n|=2n（n≥3）\n② 旋转数=n\n③ 反射数=2n-3". Directly below this box, supplementary red text reads: "后续可用数学归纳法补全证明。" The overall layout is highly structured, with clear separation between text blocks, mathematical formulas, and geometric illustrations, reflecting a meticulous and comprehensive mathematical review session.
```

### 案例 4｜3 张商品图合成家装实景

- **分类**：应用场景 · 电商
- **生成方式**：图生图（图片编辑）
- **提示词语言**：中文
- **能力看点**：多张白底商品图一键合成真实家装场景：保留家具外观材质，自动搭配软装与光影。

**完整提示词**：

```text
根据所有商品图生成真实家装效果图，仅提取家具主体，忽略价格、促销文字、品牌标识等干扰信息；必须使用全部输入商品，不得遗漏。保留家具外观、颜色和材质，自动设计协调室内背景并合理布置。可适当补充地毯、窗帘、挂画、绿植、摆件、氛围灯等协调软装，减少空墙和空地，增强空间层次与生活感。保证比例、透视、光影自然；画面需完整充满整张输出图片，不留白边或边框。不要生成电商促销主图、文字或价格信息。
```

### 案例 5｜东方古典角色设定稿（多视角一致性）

- **分类**：应用场景 · 短剧
- **生成方式**：文生图
- **提示词语言**：中文
- **能力看点**：角色设定三视图：同一人物半身特写+正/侧/背全身，多视角下五官、发型、服饰完全一致。

**完整提示词**：

```text
真实摄影, 电影级RAW原片，专业古风角色设定稿，同一人物多视角展示，画面左侧为人物半身特写，右侧依次排列正面全身、侧面全身、背面全身三视图，深灰色哑光质感背景，右侧有柔和暖调侧光光束，影棚高级氛围感；端庄冷艳的东方古典女性，乌黑长发盘成高耸发髻，脑后垂一缕长直发辫，头戴华丽金色镂空发冠镶嵌红宝石，两侧垂坠带红珠与红色流苏的步摇，佩戴同系列红宝垂坠耳饰，手腕佩戴金色宽手镯，五官立体精致，正红色唇妆，神态威严大气；身着米白色暗纹提花广袖拖地长袍，交领 V 型领口镶红色边饰，双肩配有立体镂空金色雕花肩饰，衣身延伸披风式垂坠广袖摆，腰间系宽版金色浮雕腰封，搭配红色系带与垂坠红色长流苏，衣料为高级缎面材质，垂坠感强，布料褶皱自然细腻，裙摆铺地舒展；影棚级柔和侧光，明暗过渡细腻有层次，人物光影统一，超写实真人写真质感，服化道精致考究，多视角下人物五官、发型、服饰细节完全一致，8K 超高清，极致细节，电影级古装影视质感，角色设计参考图
```

### 案例 6｜成都美食「吃货暴走地图」

- **分类**：应用场景 · 广告/海报
- **生成方式**：文生图
- **提示词语言**：中文
- **能力看点**：手绘水彩美食地图：12 个编号美食点、地标、道路河流、图例、罗盘、温馨提示的完整信息图。

**完整提示词**：

```text
画面是一张方形的手绘水彩风格成都美食地图，底色为泛黄复古纸张，带有细密纸纹和浅褐色地图线条。四周是一圈不规则藤蔓装饰边框，绿色叶片、红色辣椒、橙黄色花苞和弯曲枝条沿画面边缘环绕，形成热辣又活泼的视觉框架。左上方是醒目的主标题，红橙色粗犷手写大字写着“成都”，字形带水彩晕染和阴影，旁边点缀小辣椒、红色圆点、竖立的卡通辣椒和点赞手势小图标；标题下方用深棕色手写体写着“吃货暴走地图”，整体像旅游攻略海报的主视觉。地图主体铺满浅米色道路、蓝绿色河流湖泊和淡绿色公园色块，所有建筑、美食和地标均为俯视与小景观结合的插画形式。上方偏中位置有一个编号橙色圆点“1”，旁边的纸片标签写着“陈麻婆豆腐（骡马市店）”，下方小字写着“麻辣鲜香：百年老字号！”，标签右侧配有一碗蓝白瓷碗装豆腐菜品插图，碗中可见白色豆腐块、红油、葱花和辣椒点缀。右上方有编号橙色圆点“2”，文字为“钟水饺（总店）”，说明写着“红油水饺：皮薄馅嫩，辣而不燥！”，旁边是一碗蓝白瓷碗水饺，浅色饺子漂在红油汤汁中，碗身带青花纹样；更右侧绘有高耸细长的电视塔地标，旁边标注“339电视塔”，塔身灰蓝色，顶部有观景结构和尖塔。地图上部中间有绿色公园与亭阁，标注“人民公园”；其右侧道路区域标有“骡马市”，附近绘有传统中式建筑并标注“文殊院”。中上偏左是一大把串串香插图，竹签密集竖起，红油锅中串着红色辣椒和食材，热气以浅灰线条上升；旁边编号“3”的说明写着“春熙路·”，下一行写着“钢管五区小郡肝串串香”，再下方写着“串串蘸料的天堂！”，末行写着“一把一把停不下！”。左侧中部有宽窄巷子牌坊与小吃插图，建筑为青灰屋顶和红褐门柱，前方盘中放着三大炮小点心并冒着白色热气，文字编号“4”写着“宽窄巷子·三大炮”，说明为“甜糯弹牙，老成都的记忆！”，附近地图地名也标注“宽窄巷子”。画面中央道路区域用深色字标注“春熙路”，右侧有现代玻璃楼群和一只贴在建筑上的熊猫造型，旁边标注“IFS”；中部偏下还有一只坐姿熊猫插画，黑白配色，圆脸黑眼圈，坐在道路与绿地之间。右上至右中区域标注道路“建设路”，其上方有编号“5”的美食点，旁边是一只黑色平底锅盛放金黄色圆形蛋烘糕或煎制点心，文字写着“建设路·叶婆婆蛋烘糕”，说明写着“外酥里软，奶油馅绝绝子！”。中左偏下是一口九宫格火锅，圆形铜锅或黑锅内分成九格，红油汤底中漂着辣椒、食材和热气，编号“6”文字写着“玉林路·小龙坎火锅”，说明为“经典九宫格，越煮越巴适！”，旁边地图标注“玉林路”。右中部有编号“7”的碗装肥肠粉插图，黑色碗中装着红油汤、粉条、肥肠和葱花，文字写着“香香巷·肥肠粉”，说明写着“红薯粉Q弹，肥肠软糯入味！”，附近道路标注“二环路”。画面下方偏中左绘有“锦里”区域和传统牌楼建筑，附近还有文字“武侯祠大街”；编号“8”的位置配有一盘钵钵鸡或冷锅串串，红油盘中插着串串和食材，文字写着“武侯祠大街·钵钵鸡”，说明为“冷锅串串祖，红油味浓郁！”。右下偏中是一碗冒菜插图，深色碗中堆满豆腐、辣椒、肉片和红油食材，编号“9”文字写着“东郊记忆·冒椒火辣”，说明写着“冒菜就要冒到头！辣爽过瘾！”，其下方地图也标注“东郊记忆”，右侧大片绿地标注“塔子山公园”。左下区域有编号“10”的茶碗插图，蓝白盖碗茶由碗、盖和托盘组成，旁边写着“人民公园·鹤鸣茶社”，下一行写着“盖碗茶”，说明写着“茶香四溢，看戏摆龙门阵！”，周围是浅绿色公园色块和蓝绿色水流。更下方偏左有一碗冰粉，白色碗中盛着透明冰粉、红色果料、花生碎或糖浆，旁边散落冰块，插着绿色植物装饰；编号“11”的文字写着“锦里古街·冰粉”，说明写着“手搓冰粉，夏日必备！”，附近地图标注“锦里古街”。底部偏中位置有编号“12”的盘装兔头插图，浅色盘中放着红油麻辣兔头和辣椒，文字写着“双流老妈兔头（总店）”，说明为“麻辣入味，啃起才巴适！”。底部地图还绘有灰色小飞机图标和道路标注“机场高速路”，旁边标注“双流国际机场”，另有道路文字“三环路”。右下角是一张浅米色羊皮纸样式的图例卡片，标题写着“图例”，内部用橙色圆点、棕色地标小房子、绿色树形图标、蓝色波浪线和浅棕道路线分别对应文字“美食地点”“地标景点”“公园绿地”“河流湖泊”“主要道路”。图例右侧是一枚复古罗盘，棕色线条绘制八角星形指针，外圈为圆形刻度，上方标“N”，下方标“S”。图例下方靠右有一只拟人化红辣椒小角色，带黑色眼睛、笑脸和绿色椒蒂，旁边温馨提示文字写着“温馨提示：吃辣需谨慎，肠胃要保护~”。整张图以浅褐道路网络串联所有美食点，蓝绿色河道穿插其中，浅绿树丛与公园块面分布在各处，建筑、熊猫、美食碗盘和文字标签共同构成一张以成都吃辣文化为主题的旅游美食手绘信息图。
```

### 案例 7｜潮汕菜馆整版菜单

- **分类**：应用场景 · 广告/海报
- **生成方式**：文生图
- **提示词语言**：中文
- **能力看点**：可印刷级整版菜单：书法标题、六大栏目四十余道菜品与价格、菜品照片、印章、装饰纹样一次到位。

**完整提示词**：

```text
这是一张竖版潮汕菜馆菜单海报，整体背景为浅米色宣纸质感，带有细腻颗粒、淡墨晕染和传统中式装饰纹样。左上至左侧是一组极大的黑色毛笔书法主标题，文字为"潮菜馆"，笔触粗重、飞白明显，约占页面左侧四分之一高度区域，旁边有一条细竖线分隔，中间竖排副标语写着"潮汕风味·匠心传承"，下方配有红色方形印章，印章内为"潮味"。页面上方中部有一行圆点分隔的小字标签"潮 汕 传 统 味 · 舌 尖 上 的 鲜"，其下是英文标题"— CHAOZHOU CUISINE —"，字体为细衬线风格。英文标题下方是一段菜单介绍正文，以下为完整正文："潮菜，即潮汕菜，
是中国四大菜系粤菜的重要组成部分，
以“清、鲜、香、嫩、滑”著称，
讲究原汁原味，食材新鲜，刀工精细。"右上角是一幅淡墨水彩风格的潮汕水乡插画，画面包含远山、灰色云雾、飞鸟、河道、木船、帆船和白墙黑瓦的岭南建筑群，色彩以灰蓝、墨黑、浅褐为主，插画与背景自然融合。右上及右中还有金色祥云线条装饰，左侧中下部也有云纹装饰，左下角绘有蓝色海浪纹样，浪花为深蓝、浅蓝与米白色线描叠加，呈传统国潮插画风格。左下方有一个竖向边框信息卡，边框为浅棕色细线，带有古典角花装饰，顶部圆形牌匾写着"潮汕特色"。卡片内从上到下排列四个圆形线性图标：鱼形图标对应"新鲜食材"和"每日精选海鲜和优质食材"，蒸锅图标对应"传统工艺"和"传承潮汕经典烹饪技艺"，叶片图标对应"原汁原味"和"注重食材本味，清淡而不失鲜美"，餐盘图标对应"精致呈现"和"讲究刀工与火候，追求极致口感"。菜单主体分为多栏排版，栏目之间用细竖线分隔，标题牌匾为浅底棕色描边的云头形中式边框。中左区域的栏目标题为"潮汕冷菜"，下方菜品用黑色文字与灰色点线连接价格，依次为"潮州卤水拼盘"、"¥68"，其下小字注释"（鹅肝、鹅翅、猪舌、豆干）"；"凉拌血蛤"、"¥58"；"鱼饭"、"¥48"；"汕头鱼皮"、"¥48"；"潮式冻蟹"、"¥128"；"酸梅汁浸番茄"、"¥38"。该栏目下方嵌入一张横向圆角菜品照片，画面为白盘中的卤味拼盘，包含切片卤肉、豆干等食材，中央点缀绿色香草和紫色花朵，摄影为近景俯拍，暖色餐桌背景。中上区域栏目标题为"潮汕海鲜"，标题下嵌入一张大尺寸圆角矩形菜品照片，画面是一条清蒸鱼盛放在白色椭圆盘中，鱼身上铺有葱丝、红椒丝和姜丝，盘中有棕色酱汁，采用近景俯视角度。照片下方菜品依次为"清蒸海上鲜"、"时价"，其下小字注释"（石斑鱼/红斑鱼/老虎斑）"；"白灼虾"、"¥128"；"蒜蓉蒸扇贝"、"¥88"；"椒盐濑尿虾"、"¥108"；"潮式炒花甲"、"¥78"；"蚝仔烙蛋"、"¥68"。右上区域栏目标题为"潮汕热菜"，菜品列表依次为"潮州卤水鹅"、"¥168"；"牛肉丸汤"、"¥48"；"芋头焖鸭"、"¥98"；"潮式小炒皇"、"¥88"；"砂锅粥（蚝仔/虾蟹）"、"¥108"；"菜脯煎蛋"、"¥48"。该栏目下方有一张圆角矩形砂锅菜照片，白色砂锅中盛放带酱色的块状食材，表面点缀香菜，右侧与菜单文字对齐，照片为写实餐饮摄影风格。中下左区域栏目标题为"潮汕汤品"，标题下方是一张圆角矩形汤品照片，白色汤盅中有清汤和数颗肉丸，中心点缀绿色香菜，画面光线柔和、近景俯拍。照片下方菜品为"牛肉丸汤"、"¥48"；"鱼丸汤"、"¥48"；"猪肚汤"、"¥68"；"蛤蜊汤"、"¥48"；"冬瓜薏米汤"、"¥38"。中下区域栏目标题为"潮汕主食"，菜品依次为"潮汕砂锅粥"、"¥38"，其下小字注释"（白粥/皮蛋瘦肉粥）"；"潮汕粿条汤"、"¥38"；"炒粿条"、"¥48"；"卤水面"、"¥38"；"南瓜粿"、"¥28"；"鸭母捻（甜汤）"、"¥28"。该栏目底部有一张圆角矩形砂锅粥照片，金色双耳锅内盛有白粥，粥面有肉粒和葱花，采用近景俯拍，色调温暖。右下区域栏目标题为"潮汕小吃"，标题下方是一张圆角矩形小吃照片，白盘中摆放多块金黄色煎炸粿类小吃，旁边有绿色香菜和紫色花朵点缀，背景干净明亮。照片下方菜品依次为"潮汕蚝烙"、"¥28"；"春卷"、"¥28"；"韭菜粿"、"¥28"；"反沙芋头"、"¥28"；"粿汁"、"¥28"。页面底部中央有一条浅色长条边框装饰，内写"· 新鲜 · 传统 · 匠心 · 美味 ·"，其下方居中写着"感谢您的光临 请慢用"。右下角有红色方形印章式标识，白字为"潮味传承"。整个版面以中式菜单、国潮水墨、复古宣纸和餐饮摄影混合呈现，文字以黑色、深棕色和红色印章点缀为主，菜名与价格通过点状引导线整齐连接，形成传统而精致的潮州菜馆菜单视觉。
```

### 案例 8｜唐代女子襦裙图鉴

- **分类**：应用场景 · 广告/海报
- **生成方式**：文生图
- **提示词语言**：中文
- **能力看点**：古风知识图鉴：主视觉人物、结构拆解、材质样本、纹样色板、穿着流程图的博物馆级版面。

**完整提示词**：

```text
这是一张竖版古风知识科普海报，整体采用米白宣纸质感背景，带有浅褐色晕染、细腻纸纹和淡淡的传统花枝装饰，版面使用深棕色书法感标题、细线分隔和圆角卡片式布局，呈现出典雅专业的古代服饰图鉴氛围。顶部居中是深棕色厚重典雅的书法感大标题"唐代女子襦裙 图鉴"，右上角有浅褐色花卉线描装饰，左上有云纹线条装饰；标题下方横排副标题为"结构 · 材质 · 工艺 · 纹样 · 色彩 · 礼制"。副标题下方是一段居中的说明文字，正文内容为"襦裙是唐代女子最具代表性的日常服饰，\n由短衣“襦”与长裙“裙”组成，\n体现了唐代开放、华美、\n兼容并包的服饰风格。\n其形制在礼仪、出行、\n仕女生活中广泛使用。"。页面左侧是"结构拆解"模块，标题为深棕色，旁边有细长横线装饰，模块内沿竖向排列六个编号说明，每个编号为棕色圆点白字，旁边配有圆形服饰细节图。第一项标题为"交领襦（上衣）"，圆形特写展示浅黄色交领上衣和花纹领边，说明文字依次为"交领右衽"、"短衣齐腰"、"宽袖微阔"、"便于活动"。第二项标题为"袖（广袖）"，圆形特写展示宽大的浅黄袖口和垂坠袖身，说明文字为"平直宽袖"、"袖口宽大"、"行动飘逸"。第三项标题为"裙（下裳）"，圆形特写展示红、蓝、米色多片拼接长裙和高腰结构，说明文字为"高腰系束"、"多幅布料拼接"、"裙量充足"、"垂坠感强"。第四项标题为"腰系（丝带）"，圆形特写展示红褐色腰带、系结和垂饰，说明文字为"系于高腰处"、"打成结或流苏"、"起固定与装饰作用"。第五项标题为"披帛（可选）"，圆形特写展示浅色披帛搭在肩臂处，说明文字为"搭于双肩"、"礼仪 / 出行使用"、"增加层次与飘逸感"。第六项标题为"发饰与佩饰"，圆形小图展示女子后脑高髻和发饰，说明文字为"发髻（高髻 / 倭堕髻）"、"金银步摇"、"玉佩、香囊等"。画面中央是主视觉人物，一名年轻东亚女性全身正面站立，约占页面高度的一半以上，肤色白皙，鹅蛋脸，眉形细长，眼妆清淡，红唇妆容柔和，表情平静端庄，视线微向右侧。她梳黑色高髻，发髻体量饱满，顶部和两侧插有金色花形发簪、簪花和垂珠步摇。她身穿唐代襦裙，浅黄色交领短襦叠穿在白色内衬外，领缘和袖缘带有橙红、蓝灰、浅绿花卉纹样；下身为高腰长裙，裙幅宽大，由赭红、青蓝、米黄等多色布片拼接，表面布满宝相花、缠枝花和团纹图案，垂坠褶裥明显。腰间束有红褐色高腰系带，系带处悬挂玉佩、花结和流苏；双臂外侧披有半透明米白披帛，材质轻薄柔软，向两侧自然垂落。人物周围有细线引导到服饰部位，右侧标注从上到下写有"高髻\n唐代女子常见发式\n发髻高耸、体量饱满"，发饰标注为"发饰\n金步摇、簪花\n体现身份与审美"，上衣标注为"交领襦\n衣长齐腰\n交领右衽"，披帛标注为"披帛\n轻薄绢纱\n搭于双臂"，腰带标注为"高腰系带\n束于最细处\n突出身形"，裙装标注为"裙幅\n多片布料拼接\n形成饱满裙量"。右侧上方是"材质与工艺"模块，外框为浅棕色圆角线框，内部上半部分为六个方形材质样本，均为浅棕、米白、橙红等仿织物纹理图片。第一格标题"绢"，样本呈柔和金黄色丝织光泽，说明为"轻薄柔滑"、"透气性好"；第二格标题"罗"，样本呈棕色纱罗纹理，说明为"轻盈挺括"、"纹理细密"；第三格标题"纱"，样本为半透明浅白薄纱，说明为"轻薄透明"、"常用于披帛"；第四格标题"绫"，样本呈斜纹织物肌理，说明为"表面有斜纹"、"垂坠良好"；第五格标题"锦"，样本为橙红花纹织锦，说明为"提花工艺"、"华贵典雅"；第六格标题"纹缬（扎染）"，样本为橙蓝花叶染色纹样，说明为"植物染料"、"图案自然"。该模块下方有小标题"主要工艺"，横向排列四个圆形工艺图标，图标均为复古棕色边框和拟物纹理风格，依次为织机纹理图标，标题"织造"，说明"手工织机"、"经纬交织"；花鸟刺绣图标，标题"刺绣"，说明"平针、缠枝"、"花鸟纹样"；印版纹样图标，标题"印花"，说明"木版印"、"纹样规整"；蓝白扎染纹样图标，标题"纹缬"，说明"扎结染色"、"形成肌理"。右侧中部是"纹样与色彩"模块，标题下方有"常见纹样"，横向排列五个圆形纹样样本，分别为橙蓝花卉宝相花图案，文字"宝相花"、"富贵吉祥"；枝蔓花纹图案，文字"缠枝花"、"生生不息"；圆形团窠几何花纹图案，文字"团窠纹"、"圆满和合"；莲花叶纹图案，文字"莲花纹"、"清净高洁"；云卷线条图案，文字"云气纹"、"飘逸灵动"。其下是"唐代女子襦裙色板"，以两行圆形色块展示十种颜色：浅黄色块文字"浅黄"、"柔和日常"，月白色块文字"月白"、"清雅"，石青色块文字"石青"、"沉稳"，朱砂红色块文字"朱砂红"、"华美"，赭石色块文字"赭石"、"温暖"，黛绿色块文字"黛绿"、"高雅"，藕荷粉色块文字"藕荷"、"温婉"，绯红色块文字"绯红"、"喜庆"，米白色块文字"米白"、"素净"，驼色色块文字"驼色"、"大方"。底部左侧是一条横向流程图，标题为"穿着顺序流程图"，两端带有浅棕色折角装饰线；流程图用五个浅色人物线稿和棕色箭头连接，展示从内衣到完整襦裙的穿着过程。第一步编号"1"，标题"中衣（抹胸/中单）"，说明"贴身打底"，配图为简化女性正面线稿穿贴身中衣；第二步编号"2"，标题"裙"，说明"系于高腰处"，配图为高腰长裙线稿；第三步编号"3"，标题"交领襦"，说明"穿于最外层"，配图为穿交领上衣的线稿；第四步编号"4"，标题"系带"，说明"束于最细腰处"，配图为腰间系带的完整服饰线稿；第五步编号"5"，标题"披帛（可选）"，说明"搭于双臂或肩上"，配图为背面人物披着披帛的线稿。底部右侧是"核心特征总结"模块，浅棕色圆角框内分成左右两列图文，左列配有小圆形服饰结构图标和三组文字，第一组为"上襦下裙"、"典型“襦裙”"、"上短下长的结构"，第二组为"高腰束系"、"突出腰线"、"形成垂曳身形"，第三组为"裙量丰富"、"多幅布料拼接"、"形成飘逸垂坠感"；左下还出现圆形纹样图标旁的文字"色彩明丽"、"以浅黄、月白、石青、"、"朱砂红为主"。右列从上到下排列小图标和总结文字，第一组圆形花纹图标对应"色彩明丽"、"以浅黄、月白、石青、"、"朱砂红为主"、"体现唐代开放审美"，第二组圆形花卉纹样图标对应"纹样华美"、"宝相花、缠枝、团窠等"、"寓意吉祥富贵"，第三组圆形织造器具图标对应"工艺精湛"、"手工织造、刺绣、印花"、"体现唐代纺织高度"。整张图以教育图鉴形式呈现，文字、人物、服装细节、材质样本、图标和流程线稿都围绕唐代女子襦裙的结构、材质、工艺、纹样、色彩和礼制展开，信息布局丰满有序。
```

### 案例 9｜海岸徒步路线导览图

- **分类**：应用场景 · 广告/海报
- **生成方式**：文生图
- **提示词语言**：英文
- **能力看点**：扁平矢量运动信息图：路线图、海拔剖面、地形环形图、配速策略卡、安全提示条带的网格化版面。

**完整提示词**：

```text
This is a vertical sports and fitness infographic poster designed in a modern flat vector illustration style, utilizing a vibrant coastal color palette of ocean blues, sandy beiges, fresh park greens, and an energetic coral-orange for the primary route line, set against a clean off-white background with subtle topographic contour line watermarks. At the top center, the main title "6-Mile Marina Loop" is rendered in a bold, dynamic, slightly italicized sporty sans-serif font with a subtle wave cut-out effect on the bottom edge of the letters, colored in deep navy blue. Directly below it, the subtitle reads "The Ultimate Waterfront
Running Guide" in a clean, lightweight grey sans-serif font. Flanking the subtitle are two pill-shaped tags reading "Sunrise: 6:00 AM" and "Sunset: 6:30 PM" in white text on teal backgrounds. The central and largest visual element is a stylized top-down vector map of the Marina coastline, occupying the middle half of the poster. The map features a pale blue water area on the left and a pale beige land area on the right, separated by a smooth curved coastline. The running route is highlighted as a thick, glowing coral-orange dashed path with small white directional arrows indicating a clockwise loop. The starting and ending point is marked with a prominent coral teardrop pin at the bottom of the loop, with a label box reading "Marina Plaza
(Start/End)". Moving clockwise along the route, the path passes through a waypoint labeled "Harbor Walk", curves around a green park area labeled "Dune Park" with a small icon of sand dunes, continues up the coast past a waypoint labeled "Seawall Promenade", reaches the northernmost tip marked with a lighthouse icon and the label "Lighthouse Point", heads south along the water past "Pelican Pier" featuring a small wooden pier illustration, and returns down "Ocean Avenue" back to the start. In the top-right corner, a rounded rectangular card with a soft drop shadow displays the core route statistics, divided into four quadrants. The top-left quadrant features a running shoe icon and the text "Distance:
6.0 Miles". The top-right quadrant features a mountain peak icon and the text "Elevation:
45 Feet". The bottom-left quadrant features a stopwatch icon and the text "Time:
50-60 Mins". The bottom-right quadrant features a road surface icon and the text "Surface:
Paved & Sand". All text in this card is dark navy blue. In the top-left corner, a donut chart illustrates the surface and terrain breakdown, consisting of three segments: a large deep blue segment taking up sixty percent of the circle labeled "Paved Promenade
60%", a medium grey segment taking up thirty percent labeled "Asphalt Road
30%", and a small yellow segment taking up ten percent labeled "Packed Sand
10%". In the hollow center of the donut chart, the text "Terrain
Mix" is displayed in bold. In the bottom-left area, a smooth gradient area chart displays the elevation profile. The X-axis is labeled with "Mile 1", "Mile 2", "Mile 3", "Mile 4", "Mile 5", and "Mile 6" from left to right. The Y-axis is labeled with "0 ft", "25 ft", and "50 ft" from bottom to top. The area under the curve is filled with a light blue gradient. A specific peak at Mile 2 is annotated with a dotted line pointing to a small tag reading "Seawall Ramp", and a smaller peak at Mile 4 is annotated with a tag reading "Dune Overlook". On the middle-right side, a vertical stack of three rounded cards outlines the pacing strategy. The first card has a green left border, a walking icon, and the text "Mile 1-2:
Warm-up & Settle". The second card has a blue left border, a running icon, and the text "Mile 3-4:
Cruising Pace". The third card has an orange left border, a sprinting icon, and the text "Mile 5-6:
Strong Finish". In the bottom-right corner, a grid of three square cards highlights points of interest. The first card features a lighthouse icon and the text "Historic Lighthouse
Mile 1.5". The second card features a coffee cup icon and the text "Marina Coffee Roasters
Mile 3.0". The third card features a binoculars icon and the text "Pelican Pier Views
Mile 4.5". Spanning the very bottom of the poster is a horizontal banner with a light teal background, dedicated to runner safety and etiquette, containing three evenly spaced icon-and-text pairs. The first pair shows an arrows icon with the text "Keep right on
shared paths". The second pair shows a pedestrian icon with the text "Yield to
pedestrians". The third pair shows a water drop icon with the text "Stay hydrated
at Mile 3". The overall layout is highly structured, utilizing a clear grid system with ample whitespace between modules, ensuring all text is highly legible and the visual hierarchy guides the viewer naturally from the title to the map, then to the detailed statistics and charts, and finally to the practical tips at the bottom.
```

### 案例 10｜「安史之乱」英文教学信息图

- **分类**：应用场景 · 教育
- **生成方式**：文生图
- **提示词语言**：中文（指定渲染英文内容）
- **能力看点**：超宽横版历史教学图：概述、地图、时间线、起因与影响、历史意义，英文拼写与年份必须准确。

**完整提示词**：

```text
超宽横版英文历史教育信息图，主题为“The An Lushan Rebellion (755–763 AD)”，奶油色宣纸纹理背景，深红主标题，海军蓝、深绿、棕色分区标签，黑色高可读衬线正文。顶部左侧是唐代披甲将领安禄山插画，右侧是燃烧的古城水墨场景；标题下方摘要写“The An Lushan Rebellion was the most devastating conflict in Tang Dynasty history, shaking the empire’s foundation and marking a turning point in its decline.” 第一行左栏“OVERVIEW”列出 Time: 755–763 AD、Place: Tang Empire (modern China)、Belligerents、Leader of Rebellion: An Lushan、Outcome；右栏“MAP OF THE REBELLION”是中国地图，绿色唐帝国、红色叛军控制区，标注 Youzhou、Pinglu、Chang’an、Luoyang、Yangzhou、Guangzhou，并用红蓝箭头表示 Rebel Advance 与 Tang Counterattack。中部“TIMELINE OF KEY EVENTS”按 755、756、757、758–759、760–763 五列排列，配骑兵、燃烧城门、安禄山头像、唐军反击与收复城池插画。下方左右分别为“CAUSES OF THE REBELLION”和“IMPACT OF THE REBELLION”，用圆形图标列出 Political Corruption、Heavy Taxation、Military Imbalance、Ethnic Tensions，以及 Population Loss、Economic Devastation、Weakening of Tang、Rise of Local Powers。底部“Historical Significance”配战后古城水墨长卷。 横版约 3:1，信息图印刷品质，清晰网格，栏目对齐，英文拼写与年份必须准确；历史插画为水墨、水彩和写实漫画混合风格，红蓝绿棕配色统一。 避免文本乱码、城市位置严重错误、地图轮廓畸形、栏目重叠、字体大小无层级、现代军装、霓虹色、3D 卡通、水印。
```

### 案例 11｜意式街头暖阳人像

- **分类**：应用场景 · 人像
- **生成方式**：文生图
- **提示词语言**：中文
- **能力看点**：商业人像摄影：逆光轮廓光、胶片颗粒、浅景深街道、花束与报刊亭氛围，规避塑料感。

**完整提示词**：

```text
画面是一张竖幅户外人像摄影，整体从上到下呈现温暖的午后街景氛围。顶部左侧到上方大面积被深绿色藤蔓和橙色小花覆盖，花叶从建筑檐口自然垂落，受阳光照射的叶片呈黄绿色高光，阴影处则偏深绿，形成浓密而柔和的背景层次。左上至中上区域是一块深蓝色横向招牌，招牌表面较暗、略带磨砂质感，上面以白色哥特体大字写着“Il Messaggero”，文字位于画面左侧偏上，部分被前景花叶轻微遮挡，字体高对比、带装饰性尖角和粗细变化。招牌下方是报刊亭或书报摊的玻璃展示窗，黑色金属框架将橱窗分隔成多个矩形区域，内部陈列着许多报纸、杂志和书刊封面，但大多因景深虚化和光线反射而难以辨读，形成浅色纸张与深色边框交错的背景纹理。画面右上方是强烈的逆光区域，阳光从街道尽头照入，背景建筑被虚化成米灰色块面，边缘柔和，呈现明显的浅景深效果。画面中部偏右是一名年轻成年女性的半身至膝上人像，她回头面向镜头微笑，身体略向右转，肩背朝向观者，姿态自然放松。她有长而浓密的黑色波浪卷发，发丝被逆光勾勒出金色轮廓光，发梢在右侧向外散开，显得轻盈蓬松。她肤色白皙，脸型柔和偏鹅蛋形，眉形细致，眼睛明亮，眼妆清透，睫毛明显，面部带有自然高光，唇部为柔和珊瑚红色，笑容露齿，表情亲切明朗。她佩戴小巧耳饰，身穿黑色细肩带露背连衣裙，面料颜色深黑、轮廓简洁，细肩带从肩部向背部延伸，背部线条清晰。画面下部偏左到中部，她双手抱着一束玫瑰花，花束体积较大，主要由橙色、杏色、粉色和浅桃色玫瑰组成，花瓣层层卷曲，边缘被阳光照亮，绿色叶片和长花茎从花束下方垂出，花束与黑色裙装形成鲜明色彩对比。右侧背景是一条被阳光照亮的城市街道，地面呈暖灰与金黄色调，远处建筑、街边设施和一个模糊的红色圆形交通标志位于右下远景，均因焦外虚化而只保留色块和轮廓。整张照片采用暖色胶片感处理，带有细腻颗粒、柔和对比和明显逆光边缘光，人物位于视觉焦点，背景报刊亭、花藤、街道和阳光共同营造出浪漫、明亮、都市漫步式的氛围。
```

### 案例 12｜盛夏草帽光影薄荷水

- **分类**：应用场景 · 人像
- **生成方式**：文生图
- **提示词语言**：中文
- **能力看点**：光影斑驳人像：草帽编织孔洞的网格状投影、透明玻璃杯与薄荷水质感，附摄影参数与负面约束。

**完整提示词**：

```text
明亮盛夏户外写实人像，东亚年轻女性正面近景，黑色微卷长发，戴一顶边缘略有毛边的宽檐编织草帽，身穿白底浅蓝碎花棉质连衣裙。她双手捧着一只透明方形玻璃杯，杯中是清澈的绿色薄荷水、冰块与新鲜薄荷叶，目光直视镜头，神情柔和。正午阳光穿过草帽编织孔洞，在额头、眼睛、鼻梁、脸颊和嘴唇投下精细的网格状斑驳光影；背景为茂盛绿叶和明亮圆形散景。特写构图从帽檐到胸口，杯子位于下方前景，皮肤清透、眼睛有自然高光，清凉、轻盈、充满夏日空气感。
竖版 3:4，85mm，f/2，明亮高调曝光，清爽绿色与天蓝色配色，真实商业人像摄影，微弱胶片颗粒，细节锐利但肤质自然。
避免草帽纹理混乱、阴影方向错误、杯口或手指畸变、饮料浑浊、过曝丢失五官、假睫毛过重、文字与标识。
```

---

## 五、文中展示但未公开完整提示词的案例

以下案例文章仅展示成品图或简述，未给出完整提示词，可作为场景方向参考：

| 案例 | 说明 |
| --- | --- |
| 鲸鲨全解知识图鉴 | 一次生成完整科普读物：主视觉 + 7 大知识模块 + 全球迁徙地图 + 保护等级 |
| 复杂九宫格信息图 | 一次性生成（非拼接）3.7k token 指令；每格可独立成图；完整提示词需公众号后台私信领取 |
| 韩文时装电商广告 | 一整版韩文营销物料（知识厚实·跨语言演示） |
| 黑白日漫分镜 | 短剧/漫画产线的分镜生产力演示 |
| 美妆成分功效说明海报 | 电商图片编辑场景，原图直达成品 |

## 六、API 价格与调用信息

Qwen-Image-3.0 在阿里云百炼提供 **Pro** 与 **Standard（标准版）** 两档。文生图输入免费，未成功输出的图片不计费；新用户注册即送 10 张免费额度（有效期 90 天）。

### Qwen-Image-3.0-Pro（文生图输入免费 · 输出按分辨率计价）

| 能力 | 输入 | 输出 |
| --- | --- | --- |
| 文生图 T2I | 免费 | 1K ¥0.25 / 张；2K ¥0.5 / 张 |
| 图生图 I2I | ¥0.02 / 张 | 1K ¥0.25 / 张；2K ¥0.5 / 张 |

### Qwen-Image-3.0（1K / 2K 同价 · 更普惠）

| 能力 | 输入 | 输出 |
| --- | --- | --- |
| 文生图 T2I | 免费 | ¥0.18 / 张 |
| 图生图 I2I | ¥0.02 / 张 | ¥0.18 / 张 |

- 按量付费支持「AI 通用节省计划」抵扣：承诺金额越高、周期越长，折扣越大（首次购买用户 20/100/500 元档承诺 1 个月享 5 折、3 个月享 4.5 折；1000 元档起最高 5.3 折；活动截至 2027-03-31）。
- 体验入口：https://bailian.console.aliyun.com/cn-beijing?tab=model#/model-market/detail/qwen-image-3.0-pro

---

*本手册整理自阿里云百炼官方公众号文章，提示词为原文完整收录，仅供学习参考。*
