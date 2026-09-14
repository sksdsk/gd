import json, math, html
from pathlib import Path
R=Path(__file__).resolve().parents[1]
p=json.loads((R/'plants.json').read_text());ls=json.loads((R/'layouts.json').read_text());c=json.loads((R/'site-config.json').read_text())
esc=html.escape
colors={'CA':'#3d6650','OS':'#42664a','LI':'#86a075','HY':'#9fad89','AB':'#79966c','LM':'#6c8b63','IT':'#a9a0ba','TJ':'#3c725c'}
# All plans use the same X,Z positions as the model, with true annotated outer dimensions.
for key in ['existing','A','B','C']:
 out=[];S=44;ox=85;oy=145
 def xy(x,z):return ox+x*S,oy+z*S
 def text(x,z,t,size=14,fill='#294236',anchor='middle'):
  xx,yy=xy(x,z);out.append(f'<text x="{xx}" y="{yy}" font-size="{size}" fill="{fill}" text-anchor="{anchor}">{esc(t)}</text>')
 def rect(x,z,w,h,fill,stroke='none',dash=''):
  xx,yy=xy(x,z);out.append(f'<rect x="{xx}" y="{yy}" width="{w*S}" height="{h*S}" fill="{fill}" stroke="{stroke}" stroke-dasharray="{dash}"/>')
 def poly(points,fill,stroke='none'):
  pp=' '.join(f'{xy(*pt)[0]},{xy(*pt)[1]}' for pt in points);out.append(f'<polygon points="{pp}" fill="{fill}" stroke="{stroke}"/>')
 def line(points,stroke,width,dash=''):
  pp=' '.join(f'{xy(*pt)[0]},{xy(*pt)[1]}' for pt in points);out.append(f'<polyline points="{pp}" fill="none" stroke="{stroke}" stroke-width="{width}" stroke-linecap="round" stroke-linejoin="round" stroke-dasharray="{dash}"/>')
 title='校正后的清洁现状' if key=='existing' else ls[key]['title']
 out.append('<svg xmlns="http://www.w3.org/2000/svg" width="1320" height="820" viewBox="0 0 1320 820"><rect width="1320" height="820" fill="#f8f8f1"/><g font-family="Arial, Noto Sans CJK SC, Microsoft YaHei, sans-serif">')
 out.append(f'<text x="85" y="43" font-size="28" fill="#203e37">武汉庭院 · {esc(title)}</text><text x="85" y="73" font-size="14" fill="#6b786e">R1 · 单位 m · 外框按手写尺寸；池、门窗、通道净宽与标高仍为暂定 · 非施工放线图</text>')
 out.append(f'<defs><clipPath id="site"><rect x="{ox}" y="{oy}" width="{25*S}" height="{10*S}"/></clipPath></defs><g clip-path="url(#site)">')
 rect(0,0,25,10,'#c6c5ad','#425b4b')
 rect(.15,.15,6.75,3.8,'#bd8c77');rect(.04,7,6.92,1.6,'#b5b9af');rect(6.27,5.55,.7,3.4,'#b5b9af')
 rect(5.2,.5,13.6,.88,'#d7d5c7')
 for x in [5.6+i*.89 for i in range(15)]:rect(x-.31,.63,.62,.62,'#b0b7ae')
 if key!='existing':
  layout=ls[key]
  for surf in layout['surfaces']:poly(surf['polygon'],'#a3b488' if surf['kind']=='turf' else '#bcb49b')
  rect(17.05,2.1,.65,7.8,'#d7d5c7')
  for route in layout['paths']:line(route['points'],'#deddd0',route['width']*S)
  rect(23.45,6.42,.95,.98,'#deddd0')
 beds=['P1','P2'] if key=='existing' else ls[key]['retainedBeds']
 for i,b in enumerate(['P1','P2']):
  z=.53+i*1.56
  if b in beds:rect(.35,z,4.8,1.08,'#b5b6a8','#738275');rect(.47,z+.12,4.56,.84,'#9c9d7e');text(2.75,z+.65,b,16)
  elif key=='B':rect(.35,z,4.8,1.08,'#c49b86','#ac7d65','5 4');text(2.75,z+.65,'P2拆除 · 补砖',12)
 # Boundaries are lines; gates are approximate breaks and are never claimed to be surveyed.
 line([(0,0),(25,0),(25,5.7)],'#4d6556',2);line([(25,6.9),(25,10),(17,10)],'#4d6556',2);line([(0,0),(0,6.95)],'#4d6556',2);line([(0,8.65),(0,10),(7,10)],'#4d6556',2)
 line([(0,7.06),(0,8.54)],'#a17650',4);line([(25,5.84),(25,6.76)],'#a17650',4)
 rect(7,2.1,10,7.9,'#e0e5df','#627568','6 4')
 text(12,5.6,'建筑占位',23);text(12,6.35,'10 × 7.9 m（进深仍暂定）',15);text(12,7.0,'实际立面、凹凸与门窗位置待复核',13)
 text(12,1.12,'03 东侧通道',14)
 line([(7,6.85),(7,8.75)],'#718789',5);line([(17,3.2),(17,5)],'#718789',5)
 rect(23.675,6.59,.45,.62,'#4f5b51')
 if key!='existing':
  # Fifth-year crown outlines, third-year canopy fill; no trees invented outside the site.
  for g in ls[key]['groups']:
   pp=p[g['species']];kind=pp['kind']
   for x,z in g['points']:
    xx,yy=xy(x,z);r3=pp['sizes']['3'][1]/2*S;r5=pp['sizes']['5'][1]/2*S
    if kind in ['tree','shrub']:out.append(f'<circle cx="{xx}" cy="{yy}" r="{r5}" fill="none" stroke="{colors[g["species"]]}" stroke-dasharray="4 3" stroke-width=".8"/>')
    if kind=='climber':
     along=g['id']=='S07';rect(x-.16 if along else x-r3/S,z-r3/S if along else z-.16,.32 if along else r3*2/S,r3*2/S if along else .32,colors[g['species']])
    else:
     out.append(f'<circle cx="{xx}" cy="{yy}" r="{r3}" fill="{colors[g["species"]]}" fill-opacity="{.65 if kind in ["tree","shrub"] else .8}"/>')
    if kind=='tree':out.append(f'<circle cx="{xx}" cy="{yy}" r="2.3" fill="#354a36"/>')
   if kind in ['tree','shrub']:
    x,z=g['points'][0];text(x,z+.08,g['id'],11,'#fff')
   else:
    x,z=g['points'][len(g['points'])//2];text(x,z-.18,g['id'],10,'#284b39')
  text(21.65,4,'结缕草 '+str(ls[key]['quantities'].get('ZJ',''))+' m²' if 'ZJ' in ls[key]['quantities'] else '地被岛',12)
  text(3.2,7.91,'01 北院 · 主通路 1.6 m',13)
  text(21.3,6.6,'02 南院 · 通路约1.2 m' if key!='C' else '02 南院 · 环路约1.15 m',12)
 else:
  text(3.5,5.4,'01 北院',22);text(21,4,'02 南院',22);text(3.4,7.92,'灰路宽 1.6 m · 位置暂定',12)
 out.append('</g>')
 # Dimension annotations.
 line([(0,-.48),(7,-.48)],'#6d8270',1);text(3.5,-.64,'7 m',15)
 line([(7,-.48),(25,-.48)],'#6d8270',1);text(16,-.64,'18 m',15)
 line([(17,10.45),(25,10.45)],'#6d8270',1);text(21,10.86,'8 m',15)
 line([(26,0),(26,10)],'#6d8270',1);text(26.7,5,'10 m',15)
 text(-1.2,5,'N 北',16);text(26.2,10.8,'S 南',16);text(12.5,-1.1,'E 东',14);text(12.5,10.86,'W 西',14)
 out.append('<text x="85" y="681" font-size="14" fill="#304e3b">实填冠幅：第3年　虚线冠幅：第5年　所有生长均为管理目标示意，不是保证值</text>')
 codes=['CA','OS','LI','HY','AB','LM','IT','TJ']
 for i,code in enumerate(codes):
  x=85+(i%4)*293;y=718+(i//4)*31
  out.append(f'<circle cx="{x+7}" cy="{y-4}" r="6" fill="{colors[code]}"/><text x="{x+23}" y="{y}" font-size="12" fill="#3f5745">{code} · {esc(p[code]["name"])}</text>')
 out.append('<text x="85" y="790" font-size="12" fill="#7d755e">图内 N / S / E 编号为植物组号；逐组坐标、数量与株距见设计说明。方位字母标在图框外。</text></g></svg>')
 (R/'assets'/f'plan-{key}.svg').write_text(''.join(out))
(R/'assets/plan.svg').write_text((R/'assets/plan-existing.svg').read_text())
(R/'assets/measurement-sheet.svg').write_text((R/'assets/plan-existing.svg').read_text())

def table(head,rows):return '<div class="table-wrap"><table><thead><tr>'+''.join('<th>'+esc(x)+'</th>' for x in head)+'</tr></thead><tbody>'+''.join('<tr>'+''.join('<td>'+str(x)+'</td>' for x in row)+'</tr>' for row in rows)+'</tbody></table></div>'
def link(url,title):return f'<a href="{url}" target="_blank" rel="noopener">{title}</a>'
def section(id,title,body):return f'<section id="{id}"><h2>{title}</h2>{body}</section>'
parts=[]
parts.append(section('reconstruction','01 / 现状重建与尺寸校正','''<p>以13张照片及约57秒连续视频建立空间关系，再用你的手写图校正外框。视频依次经过南侧裸土院、东侧通道和北侧种植池院；部分航拍图可能较早，拍摄日期未核实。模型清除了临时袋子、工具、板材、活动盆栽与菜架；灰色墙面板件、百叶、管线和原有轻型拱架仍作为固定或待确认构件保留。</p><img class="plan" src="../assets/plan-existing.svg" alt="清洁现状平面图">'''+table(['项目','本版采用','依据 / 限制'],[
['总外框','25 × 10 m，250 m²','25 m = 7 + 18；按图包含建筑占位，不是250 m²净花园'],['北院 / 南院','7 × 10 m / 8 × 10 m','用户手写尺寸'],['建筑 / 通道','建筑长10 m；通道沿墙长约10 m','25−7−8=10；侧宽暂2.1 m，建筑进深暂7.9 m'],['室外面积','约171 m²','以矩形建筑79 m²相减；凹凸与通道宽变化会改变面积'],['北院红砖区','约7 × 4 m','4 m按东端区域深度解释；不是池体尺寸'],['主灰路','宽1.6 m；中心Z=7.8 m暂定','左边4 / 5 / 1.6 m分段不能与总10 m直接闭合'],['P1 / P2','各4.8 × 1.08 × 0.55 m；池间约0.48 m','仍为影像比例估值；壁厚、土深、底板与出水口未量'],['模型坐标','X正向为南；Z正向为西；Y向上','原点在北/东围栏角；平面图左北、右南、上东、下西']])+'<p>已辨认到的现有植物以菜作、攀援与自生覆盖为主，无法凭影像可靠鉴定树种。围栏外的大树及灌木不能视为自家可拆植物，也未虚构为确定遮阴体量。保留价值需通过全株、树干、叶片近照与归属核实。</p>'))
parts.append(section('uncertainty','02 / 尚未校准的局部',table(['未知项','当前处理','解决证据'],[
['“5 m”标记两端','不强行拉伸10 m总宽；继续使用Z=7.8 m灰路中心','一条注明端点的尺寸线即可'],['侧通道最窄净宽','围栏到墙2.1 m；踏步0.62 m，碎石带0.88 m','墙凸、窗开启后净宽及百叶维修要求'],['建筑高度与门窗','高12.8 m占位，开口仅示意','首层尺寸串、窗门宽高、层高照片'],['池体及池底','不把混凝土底板画成已知；B拆P2范围暂按5.18 m²','池外长宽高、土深、排水孔与局部探查'],['标高与排水系统','平模型，只标可见格栅；不编造地下管道','门槛/路面/格栅/管底标高，雨后照片与出水去向'],['邻窗与植物遮阴','视线按代表方向测试，非邻居精确坐标','从目标房间、院门和围界约1.6 m眼高拍照；标邻窗高度'],['土壤、根域及供货','地栽与排水均为实施条件，品种需核苗','土层、pH、渗水检查；苗圃品种标签及实物尺寸']])+'<p class="callout">这些未知项不会阻断本轮设计比较；它们影响施工放线、排水和最终采购。模型不是测量成果，也没有宣称隐藏部分已校准。</p>'))
parts.append(section('concept','03 / 总体概念：林缘、花带、留白','''<p>借用英式花园的空间语言：有深度的边缘、重复的植物群、经过控制的花色和开放的地面。主色为不同深浅的绿色，白花提供季节亮点，鸢尾与山麦冬带少量柔紫。成熟后的冠幅比第一天的“满铺”更重要。</p><p>北院承担最完整的常绿主景；南院以两株小乔木和夏花回应，中心保留活动与观赏余地；东侧通道沿低叶带连续，百叶和管线前留空。活动椅可以临时搬入。设计没有固定坐凳、餐桌区、厨房或新增凉棚。</p><img class="hero-image" src="../assets/preview-B3.png" alt="B方案第3年实际GLB几何预览"><p class="caption">由实际GLB几何生成的示意预览，建筑作低位剖切以看清庭院；不是照片合成。网页可显示完整建筑。</p>'''))
rows=[
['空间与外观','双长池形成平行花带；南院矩形草坪与直线通路','P1成为边界花带，内侧空间打开；北院林缘与南院轻折通路呼应','低连续花境替代双池；南院地被岛与环路，地面更整体'],
['平衡与视觉重量','仍有两道高墙；以统一浅暖灰矿物质修补面、低叶片弱化','保留一条记忆，减少中间阻挡；本案综合最均衡','减少高池体量最多，但要控制植物总量，避免满院灌木'],
['通行','池间约0.48 m不是主路；走池端和原有灰路','P2拆后约5.18 m²重获平地；接北院1.2 m连接路','北院连通花境占去原砖面一部分，外侧通路仍要保留；南院环路最长'],
['隐私','茶梅与局部络石承担；低矮双池本身不提供完整隐私','集中屏蔽关键低层视线，中央保留深度','北院增加两株地栽茶梅，有更多屏蔽深度，夏季通风须保留'],
['种植潜力','池内只种低宿根，土深和排水有约束；两条花带可重复','P1宿根带+主要地栽灌木；拆一池不被迫增加高维护植物','约14 m²连通地栽区可改善根域；前提是起砖并处理原池基'],
['长期维护','两池易够到，但窄缝积叶清理繁琐；草坪需剪','一个池易管；两株树、少量绣球和小草坪属于低至中等维护','无割草任务，但环路边缘与较多地被在前两年更需除草'],
['施工干预','双池检查排水、修补表面；两院铺装大体保留','拆P2、局部补红砖；P1修补及排水改善；新增短连接路','双池拆除、局部起砖、地栽土壤改善；南院环路铺设较多'],
['相对成本','通常最低；若双池排水/开裂严重，可能不便宜','通常中等；受拆池清运、地砖可配性及暗埋构造影响','通常最高；不割草的后期节省不能抵消所有土建增量'],
['主要优点','改造小，保留最多；适合预算严且池体状态好','通行、视觉重量、铺装保留与种植量之间最平衡','地面和根域最连贯；适合明确不愿保留任何高池的家庭'],
['主要缺点','双池体量仍在，不能仅靠植物“消失”','需施工修补且存在色差；一个池仍需维护','拆改最多、初期土面最大；排水和地下结构风险暴露更多']]
parts.append(section('alternatives','04 / A、B、C 的结构性比较',table(['维度','A 保留双池','B 保留P1，拆P2','C 拆除双池'],rows)+'<div class="three-plans">'+''.join(f'<a href="../assets/plan-{k}.svg"><img src="../assets/plan-{k}.svg" alt="方案{k}平面图"></a>' for k in 'ABC')+'</div><p><b>相对成本是设计判断，不是武汉施工报价。</b>三案共同的土壤改善、苗木、灌溉与新增连接路先作为同一基础报价，再分别列池修补/拆除、清运、补砖、环路、排水改造。不要用一口价掩盖不可见的池底工程。</p>'))
parts.append(section('masterplan','05 / 推荐主方案 B','''<p><b>推荐保留靠东侧围栏的P1，拆除靠院子内侧的P2。</b>理由是它释放了双池中更靠中心的一道障碍，同时保留一条与东侧通道方向一致的植物带。若P1探查发现封底且无法改善排水，或修复报价接近整体重做，应重新优先比较C。</p><img class="plan" src="../assets/plan-B.svg" alt="B推荐主平面图"><p>北院：P1用两列低宿根统一；茶梅在地栽区形成常绿背景，三株白花绣球置于较凉处。北院新连接路目标宽1.2 m，接回原1.6 m灰路；不强迫人穿过窄池缝。西边界以约3 m长的络石分段屏障作局部背景。</p><p>南院：桂花置于东半部，白花矮紫薇置于西半部；中心约9.7 m²结缕草保持低矮留白。约1.2 m通路连接侧通道、主要入户开口和院门；格栅周围留可揭检修的铺面。两株树均地栽，不放进未知土深的高池。</p><p>东侧通道：保留原踏步/碎石及窄边砖，不扩大成大露台。沿墙仅局部重复山麦冬；百叶前X约10–14 m段留空，藤本不攀房屋。方板0.62 m与碎石带0.88 m不能宣称满足所有通行需要：施工前检查最窄净宽，必要时只把脚下松动碎石整平、稳固，保留排水能力。</p><p>现有金属拱架只按现状存在建模。是否继续利用取决于锈蚀、固定与净高；它不构成新增遮棚，也不计划用密集藤叶封闭整条通道。</p>'''))
climate='https://www.wuhan.gov.cn/zjwh/whgk/202004/t20200414_999422.shtml'
parts.append(section('climate','06 / 武汉气候与日照逻辑',f'''<p>武汉属北亚热带湿润季风气候，夏热冬冷、雨水季节集中。市政府概况列年均温16.9–17.5°C、年降水1228–1389 mm，约40%降水集中在6–8月；这些是官方概况范围，页面未注明统一的气候常年值统计期。2024年既出现强梅雨，也出现夏秋旱情，所以“雨多”不等于不需浇水。{link(climate,'武汉市政府：武汉市概况')}</p><p>本案应对：雨季用疏松但不松散漂移的覆盖物、畅通排水和分组通风；夏季重点保护新根球和少量绣球；冬季依靠茶梅、桂花、络石及山麦冬维持结构。避免把耐寒性仅到轻霜的品种、需干爽夏季的英式花境植物作为骨干。</p>'''+table(['区域','方位带来的推断','仍需核实'],[
['北院','建筑在其南侧，冬季更可能有长时段遮阴；适合以半阴林缘为设计条件','北院不等于夏季全天阴。西晒强的位置不硬放绣球；茶梅优先局部下午遮阴'],['南院','建筑在北侧，夏季具备更强日照潜力；可承担紫薇和小草坪','邻树/相邻楼栋可能减少实际日照；草坪先记录数日直射时长'],['东侧通道','早晨可能见光、下午受本体建筑遮阴；能形成较凉过渡','墙角风口、百叶排热和遮挡必须逐段观察']])+f'''<p>仅用建筑高12.8 m占位、武汉纬度约30.6°和水平地面作太阳正午几何估算：夏至向北影长约1.6 m，春秋分约7.6 m，冬至约17.7 m。计算式为 H / tan(太阳高度角)。<b>这是建筑体量假设的敏感性演示，不是实际日照小时数</b>；高度、邻楼和树冠变化会改变结果。网页阴影是查看空间的示意日光。</p><p>茶梅与络石在武汉有直接栽培展示依据：{link('https://www.wuhan.gov.cn/sy/whyw/202412/t20241220_2506110.shtml','武汉本地茶梅冬季展示')}；{link('https://www.wbgcas.cn/KPPJ/zrjy/hbsjt/201605/t20160506_4597016.html','中科院武汉植物园：络石')}。其他植物依据原产分布及权威园艺资料筛选，仍须采购本地露地驯化苗，不能将海外栽培资料当作武汉每个角落的表现保证。</p>'''))
rows=[]
for code in ['OS','CA','LI','AB','HY','TJ','LM','IT','ZJ']:
 a=p[code];q=ls['B']['quantities'].get(code,0);rows.append([f'<b>{code} · {esc(a["name"])}</b><br><i>{esc(a["botanical"])}</i>',str(q)+(' m²' if code=='ZJ' else '株'),esc(a['stock']),esc(a['mature']),esc(a['flower']),esc(a['light']),link(a['source'],'资料')])
parts.append(section('plants','07 / 推荐方案植物表与采购规格','<p>固定为八种观赏植物加一种草坪草，采用重复组团；不是每处换一种。规格是建议的入场苗尺度，数量是模型净量，不包含损耗。Acoma需核实本地库存；若改用本地白花紫薇，必须核对成熟体量及抗病性，不能直接用普通高大品种替换。</p>'+table(['代码 / 名称','B净量','建议入场规格','成熟与管理尺度','花期约值','光照','来源'],rows)+'<p>“阔叶山麦冬”在市场可能被笼统叫麦冬，须按 <i>Liriope muscari</i> 核苗。白花茶梅、白花绣球需看品种标签或花期母本；不按网络图片保证花色。未采用依靠常换草花、频繁喷药的玫瑰墙或精修黄杨球阵。</p>'))
rows=[]
for g in ls['B']['groups']:
 a=p[g['species']];rows.append([g['id'],str(g['zone']),esc(a['name']),str(g['quantity']),str(a['spacing'])+' m',f'X {min(t[0] for t in g["points"]):g}–{max(t[0] for t in g["points"]):g}<br>Z {min(t[1] for t in g["points"]):g}–{max(t[1] for t in g["points"]):g}',esc(g['note'])])
parts.append(section('spacing','08 / 植物组、株距、数量与放样','<p>坐标原点见平面图：X向南、Z向西，单位m。图中每个植物位置与下表、GLB来自同一份数据；详细逐株点位保存在 <a href="../layouts.json">layouts.json</a>。表中范围用于定位植物组，<b>不是已实测的施工坐标</b>。</p>'+table(['组号','区域','植物','数量','建议中心距','点位范围','本组说明'],rows)+'<p>山麦冬/鸢尾约0.4 m；绣球约1.4 m起；茶梅约2.1 m；六道木约1.5 m；络石约1.5 m。树木按3–3.5 m最终冠幅预留，但墙边或邻树限制会改变树位。灌木层允许叶冠边缘轻叠，根颈不可埋入厚覆土；保留枝叶离路、格栅及检修面的余量。</p><p>P1暂定净种植宽约0.84 m，两列植物采用约0.44 m列距，沿长向各11丛，总22丛。最终池内净宽若不足，应减为一列，不以挤压根系保持数量。草坪9.69 m²为净面积，采购通常另加约5–10%裁切余量；苗木不提前加密“凑满”，先核规格再订货。</p>'))
parts.append(section('privacy','09 / 分段隐私：先判断视线，再决定高度',table(['观察方向','应对位置 / 元素','效果与残余'],[
['北侧公共路径 → 北院主景','N10茶梅与前层植物，保持非连续边界','第三年开始缓冲低层视线；第一年冠幅不足，不能宣称即时完整隐私'],['西侧邻院 → 北院窗口','N14络石限高约1.9 m、总长约3 m','遮关键小段，余处保留开口与纵深；冬季比落叶灌木可靠'],['南侧路径/邻院 → 南院','桂花、六道木错位成层；南界西端S07络石','桂花提供较高常绿冠层，络石补低位。六道木冬季可能落叶，不能作为唯一屏障'],['院门打开 → 房屋','保留通行，利用偏折的南院通路减少直线贯穿','打开的北院门仍可能沿灰路直视房屋，无法靠两旁绿植完全消除'],['周边上层窗 → 两院','小乔木仅选择性遮住部分角度，核实窗口后小幅移位','高层俯视仍存在；不为遮挡所有高层窗栽连续高墙式树篱'],['房屋自身向外看','低宿根在前、灌木中层、小树在侧；百叶前留空','保留光线、出入口和检修视野，不把树冠贴在玻璃上']])+'<p>视线高度可用直线插值核实。例如<strong>纯示例</strong>：界外3 m处有6 m高窗，界内4 m处目标视点高1.5 m，则围界处视线约4.07 m高，1.9 m络石无法阻挡。现场若真有此类窗口，应在靠近目标处用树冠局部遮挡，并结合室内轻帘；本模型没有虚构这扇邻窗的位置。</p><p>现有围栏承受藤本后风荷载增加，支撑需检查。采用窄段、可修剪的络石，植物不攀燃气/用途未明管线，不堵门扇，不以公共绿化提供“保证隐私”。</p>'))
parts.append(section('seasons','10 / 四季兴趣与冬季诚实呈现',table(['时段','主体','本案取舍'],[
['春（约3–5月）','鸢尾、络石白花，常绿新叶','同一物种分段重复；网页是季相组合，非保证同日齐开'],['夏（约6–8月）','矮紫薇白花、绣球前段、山麦冬紫穗，深浅绿叶','少量花色与阴影；高温期不追求天天满花'],['秋（约9–11月）','桂香、六道木零续开花、紫薇秋叶，茶梅渐入花期','花期随品种和年份变化；以绿叶状态为常态'],['冬（约12–2月）','茶梅与桂花、络石、山麦冬保持骨架','紫薇/绣球落叶，六道木可能落叶，草坪变稻草色；网页冬季按较冷情景显示']])+'<p>每株的生长尺寸与物候不是同步的时钟。网页春夏秋冬按钮展示大致季相；不表示一株茶梅连续开整个冬季，也不表示夏花全在同一天开放。不开花时仍靠叶片、树干、群落轮廓和红砖关系维持画面。</p>'))
parts.append(section('drainage','11 / 排水、根域与保留铺装','''<p>现状格栅保留，在南院通路旁留约0.95 × 0.98 m可接近的检修铺面。模型没有地下管道或确定坡箭头，因为格栅的性质、管底标高与最终出口还未知。所有新增材料尽量与保留砖面平接，不把水推向门槛。</p><ol><li>先用水平测量建立门槛、铺面、树池土面和格栅标高关系，确认合法出水路径。参考约1–2%的面层找坡仅作初步设计范围，最终依材料、距离及实测落差确定；不能未经核实直接按1%施工。</li><li>清理落叶、淤泥与现有排口，雨后记录积水位置和消退时间。原砖若积水，优先局部揭铺调基层，不为保留每块原位砖而牺牲排水。</li><li>探查P1是否通土及底部积水。宿根带希望有至少约25–30 cm有效疏松土层并保持排水；这是本案目标而非当前已知。出水孔不能直接排到易打滑通道上。</li><li>B拆P2时先定位暗埋设施，再分段拆墙、清运、确认基底。原位土、回填或底板三种情况对应不同补砖做法；不可在松土上直接薄铺砖面。</li><li>C须把原池底和连接处局部铺装处理为真正连通的可种植土层。只盖一层土在整片混凝土上，不能支持模型里的地栽灌木。</li><li>树木根区要连接到足够土量的原土带，避基础、管线与检查井。若浅层全是施工废料，先改善连续根域或减少树木；不把孤立深坑当排水方案。</li></ol><p>不要默认在黏土坑底铺一层碎石就能“排水”；若没有可用出水路径，它仍可能成为积水盆。也不盲目往重黏土里少量掺沙。按渗水、土质和出口条件决定整体土壤改善、浅沟/暗排或抬高种植面。</p><p>花境表面铺约4–5 cm有机覆盖层并远离根颈；墙边防潮和白蚁检查要求以房屋做法为准。地面标高不得埋没防潮层、透气口、排水孔。覆盖物用量按实际花境净面积乘厚度计算，不能拿171 m²全部计入。</p>'''))
rows=[]
for code in ['OS','CA','LI','AB','HY','TJ','LM','IT']:
 a=p[code];rows.append([esc(a['name']),esc(a['water']),esc(a['care'])])
parts.append(section('maintenance','12 / 把养护量控制在普通家庭能承担的范围','''<p>主方案的维护水平是<strong>低至中等</strong>：有小草坪、三株绣球和少量藤本，因此不是“种下就不用管”。用重复地被减少长期裸土，用自然冠形减少频繁修球；不设水景、季节草花更换区或需要爬高修剪的整面藤墙。</p><p>浇水按根区而非日历：前几周每1–2天检查根球和周边土，缺水才浇透；降雨后暂停，防止根球内外干湿不同。夏季高温/风口更勤检查，成活后延长间隔、加深单次湿润。绣球与树木/耐旱地被分阀，优先可过滤、能冲洗的滴灌或滴水管。没有土壤和滴头流量资料，不提供虚假的固定“每株每天几升”。</p>'''+table(['植物','水分管理','养护要点'],rows)+'''<p>梅雨期避免傍晚频繁喷叶、过量氮肥和把叶冠挤成不透风的墙。巡查叶斑、白粉、介壳虫、烂根，先改善水分与通风、去除病残组织，确诊后才选择本地登记允许的处理方式，不制定全年预防性喷药套餐。抗病品种表示风险较低，不是免疫。</p><p>小草坪生长季通常7–14天检查修剪需求，遵守一次不去掉超过约1/3叶长；按结缕草实际长势调整。冬季休眠，不用黑麦草覆播维持假常绿。若实测光照明显不足，把草坪改成同一种山麦冬即可延续语言，约0.4 m网格需增约60丛（扣除边界与树根后复核）。</p>'''))
rows=[]
for code in ['OS','CA','LI','AB','HY','TJ','LM','IT']:
 a=p[code];rows.append([esc(a['name'])]+[f'{a["sizes"][str(y)][0]} × {a["sizes"][str(y)][1]}' for y in [1,3,5]])
parts.append(section('growth','13 / 第1、3、5年：允许花园逐步成形','<p>模型按表中的建议入场苗起算。尺寸是健康建植、正常浇水、适度疏剪下的<strong>示意管理目标</strong>；不是生长率测量或保证，不按统一倍数放大所有植物。每组根系、苗源和实际光照会改变结果。</p>'+table(['阶段','空间样子','维护重点'],[
['第1年','灌木之间有明显空隙，地被尚未闭合，络石不完全遮挡','覆盖土面、除草、检查根球水分、牵引枝条；不通过多买大灌木强行填满'],['第3年','茶梅与绣球开始形成层次，地被连片；南院树冠仍相对轻','开始选择性疏枝，确认实际视线；检查通道边缘是否受侵占'],['第5年','树冠及灌木成为空间主体，前后层轻叠，局部需要分株','保留通路净宽，分株山麦冬/鸢尾，疏灌木基部；按管理冠幅维护而非逐年变大']])+table(['植物','第1年 高×幅 m','第3年 高×幅 m','第5年 高×幅 m'],rows)+'<img class="hero-image" src="../assets/preview-B5-winter.png" alt="B方案第5年冬季示意"><p class="caption">B · 第5年冬季：保留常绿骨架，落叶木本露枝，草坪呈休眠色。实际冷暖年份会改变叶况。</p><p>第五年不等于所有植物自然成熟的终点。桂花、茶梅未经管理会继续长大；种植表已区分天然潜力与本案控制尺寸。若需要连续重剪才能塞进场地，应该减少或换小体量品种，而不是长期依赖强剪。</p>'))
parts.append(section('calendar','14 / 基本年度养护表',table(['时间 / 触发','工作','频率提示'],[
['1–2月','查排水和冻损；茶梅花后再决定轻剪，不齐剪所有常绿','雨后检查；寒潮后观察，不立即重剪未确认死枝'],['2–3月','紫薇轻疏交叉枝；山麦冬新芽前清旧叶；六道木疏老枝','集中一次，按物候调整'],['3–4月','土壤温度合适时补植、少量堆肥或按检测施肥；查灌溉滴头','建植缺株补齐，不全面重复施肥'],['4–5月','花后整理络石与鸢尾残梗，开始草坪生长观察','藤本不让其触及百叶、窗与管线'],['6–7月 梅雨','疏通格栅，检查积水、叶斑和根腐；雨够时停灌','大雨前后检查，湿热期每周巡看'],['7–9月 热旱','晨间查土与根球、必要时深灌；草坪按长势修剪','新植苗可需每日检查；成活后不是每日固定浇'],['9–10月','桂花观花后轻疏；藤本限界；条件适宜时分株和秋植','不在临寒前用高氮催嫩梢'],['11–12月','收集病叶、清理窄缝及格栅，适度补覆盖物','保留正常冬季骨架；不将落叶灌木全部剪平'],['第3–5年及以后','地被拥挤时分株，校正树冠/屏障宽度与实际视线','按拥挤触发，而非机械每年分株']])+'<p>家庭工作量的主要峰值在建植、梅雨检查和夏季水分/割草。每次庭院巡查顺便检查枝叶是否侵入门扇、窗扇和通路，比年底一次性重剪更容易维持质量。</p>'))
parts.append(section('handover','15 / 模型、网页和实施交接','''<p>主文件 <a href="../models/garden.glb" download>garden.glb</a> 为推荐B方案第3年夏季示意，采用米、Y向上；现状独立保留，A/B/C各含第1/3/5年。架构、铺装、围栏、池体、植物组与季节叶花对象按名称分组；植物信息在GLB extras与JSON中保留。花期切换由网页读取元数据实现，普通GLB查看器默认只显示夏季状态。</p><p>模型使用程序化低多边形几何和嵌入PBR颜色材质，无需外部贴图。它不是摄影测量，叶片与开花为示意；不能将模型识别成具体苗木的真实枝形。建筑默认在网页中作剖切以看清花园，勾选“完整建筑体量”可恢复。</p><p>网页是纯静态Three.js项目，无后端、无第三方CDN字体或运行库依赖；每次仅加载选定方案/年份，降低移动端首次流量。旋转、缩放、双指平移、点选植物、俯视和区域视角均可用；阴影默认关闭，可按性能打开。网页提供无法启动WebGL时的平面图替代。</p><p><a href="../downloads/garden-viewer-R1.zip" download>下载完整项目 ZIP</a>，解压进入garden-viewer目录后执行 <code>python -m http.server 8000</code>，浏览器访问 <code>http://localhost:8000</code>。不能直接双击index.html读取模型。可将解压后的静态内容部署到支持静态文件的服务；自行公开部署时注意其中包含自家院落照片。</p><p>交接先顺序完成：①复核剩余尺寸与排水；②按A/B/C分项报价；③确认P1探查结果后选定拆改；④放样树冠和通路；⑤土壤改善与硬景施工；⑥适季种植、验苗与养护交接。正常家庭应先把排水和通行做好，再追求花量。</p><p class="callout">验证范围：已进行代码语法、静态资源引用、GLB解码、方案/数量/年度几何一致性检查，并从实际模型几何生成预览。未进行iPhone、iPad、Android实机或浏览器交互测试；移动适配按响应式布局与Three.js触控机制实现。</p>'''))
css='''*{box-sizing:border-box}body{margin:0;background:#f4f5ef;color:#2d4437;font:16px/1.85 system-ui,-apple-system,"PingFang SC","Microsoft YaHei",sans-serif}header{padding:48px max(24px,calc((100vw - 1140px)/2));background:#203e37;color:#eef1e9}header h1{font:38px/1.4 Georgia,"Songti SC",serif;margin:10px 0}header p{max-width:750px;color:#d0dccc}header a{color:inherit}nav{display:flex;flex-wrap:wrap;gap:8px 20px;padding:24px 0;border-bottom:1px solid #ccd6c8}nav a{font-size:13px}main{max-width:1190px;margin:auto;padding:0 24px 60px}section{margin:44px 0}h2{font:27px/1.5 Georgia,"Songti SC",serif;border-bottom:1px solid #bdcbbd;padding-bottom:12px}h3{font-size:18px}p{max-width:1100px}a{color:#396447;text-underline-offset:4px}.plan{display:block;width:100%;height:auto;background:white;border:1px solid #d5ddcf;margin:24px 0}.hero-image{width:100%;height:auto;display:block}.caption{font-size:12px;color:#73806d;margin-top:8px}.table-wrap{overflow-x:auto;margin:22px 0}table{border-collapse:collapse;width:100%;font-size:13px;line-height:1.7;background:#fff;min-width:620px}th,td{padding:12px 13px;text-align:left;vertical-align:top;border:1px solid #d5ddcf}th{background:#e5ecdf;font-weight:600}td:first-child{min-width:105px}tr:nth-child(even){background:#f8faf4}td a{white-space:nowrap}.callout{background:#e8eddf;border-left:3px solid #7e946e;padding:18px 22px}.three-plans{display:grid;grid-template-columns:repeat(3,1fr);gap:12px}.three-plans img{width:100%;border:1px solid #c8d5c0}code{background:#e2e8dc;padding:2px 5px;font-size:14px}li{margin:10px 0}footer{padding:24px;text-align:center;color:#76826f;font-size:12px}@media(max-width:650px){header{padding:30px 20px}header h1{font-size:30px}main{padding:0 16px 36px}body{font-size:15px}h2{font-size:23px}.three-plans{grid-template-columns:1fr}section{margin:34px 0}}@media print{body{background:#fff;font-size:10pt}header{padding:14mm;color:#203e37;background:#fff}header p{color:#53694f}header h1{font-size:26pt}main{padding:0 8mm;max-width:none}nav,.no-print{display:none}section{break-before:page;margin:0}h2{font-size:18pt}table{min-width:0;font-size:8pt}th,td{padding:6px}tr{break-inside:avoid}.table-wrap{overflow:visible}.plan{max-height:170mm}a{color:#36583e;text-decoration:none}.three-plans{display:block}.three-plans img{max-height:65mm;width:auto}footer{display:none}}'''
nav=''.join(f'<a href="#{id}">{title}</a>' for id,title in [('reconstruction','现状'),('uncertainty','假设'),('alternatives','方案比较'),('masterplan','主方案'),('climate','武汉气候'),('plants','植物表'),('spacing','株距/数量'),('privacy','隐私'),('seasons','季相'),('drainage','排水'),('growth','生长'),('calendar','养护'),('handover','下载与运行')])
body=f'<!doctype html><html lang="zh-CN"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>武汉庭院 · 完整设计说明 R1</title><style>{css}</style></head><body><header><a href="../index.html">← 返回三维庭院</a><h1>两院一径 · 设计说明</h1><p>英式空间语言，武汉的植物与季节。现状、三案比较、推荐主方案、种植与维护的完整交接。</p><span>R1 · 2026年9月14日 · 以现有模型及手写尺寸为基础</span></header><main><nav>{nav}</nav>'+''.join(parts)+'</main><footer>来源检索：2026-09-14。园艺资料为适生性依据；设计尺寸、数量与取舍为本案推演。</footer></body></html>'
(R/'docs/design.html').write_text(body)
(R/'docs/review.html').write_text('<!doctype html><html lang="zh-CN"><meta charset="utf-8"><meta http-equiv="refresh" content="0;url=design.html#reconstruction"><title>现状重建已更新</title><a href="design.html#reconstruction">查看校正后的现状重建 R1</a></html>')
print('Generated 4 matching SVG plans and full 15-part design documentation.')
