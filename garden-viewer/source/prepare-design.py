import json, math
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def write(name,data): (ROOT/name).write_text(json.dumps(data,ensure_ascii=False,indent=2))
c=json.loads((ROOT/'site-config.json').read_text())
c.update(revision='R1 · measured envelope / concept design',status='CONCEPT — annotated dimensions + explicit proxies; not construction survey',north=[-1,0,0],coordinateNote='Metres, Y up. +X = south, +Z = west; north is left and east is top on plans. Origin: north/east fence corner.')
c['dimensions'].update(planterCourtDepth=7,bareCourtDepth=8,planterApronDepth=4,mainRouteWidth=1.6,mainRouteZ=7.8)
c['dimensionStatus']={'envelopeLength':'25 m = annotated 7 + 18 m; includes building proxy','envelopeWidth':'10 m from annotated east–west envelope','planterCourtDepth':'7 m annotated north courtyard','bareCourtDepth':'8 m annotated south courtyard','planterApronDepth':'4 m annotated east portion of north courtyard','mainRouteWidth':'1.6 m interpreted as gray access route width','sideStripWidth':'2.1 m PROXY; blue E is orientation, not a measurement','mainRouteZ':'7.8 m PROXY; 4 m / 5 m / 1.6 m dimension chain does not close','allOtherValues':'Visual proxies, not survey values. Individual planter sizes and elevations remain unmeasured.'}
c['groundLevels']='R1 remains flat. Heights of thresholds, paving, drain grate/invert and actual falls are unknown.'
updates={
'zone1':('北院 7 × 10 m，东侧红砖区进深 4 m；灰路宽按 1.6 m。通路中心 Z=7.8 m 暂定。','补测“5 m”的两端及灰路距东西围栏的位置；不再重复索要已标注的外框尺寸。'),
'zone2':('南院 8 × 10 m；墙角和门的位置仍为影像估值。','只需核实门洞、格栅及首层开口相对墙角的位置。'),
'passage':('沿建筑长约 10 m；围栏至墙仍暂取 2.1 m。蓝色 E 是东方标记，不是通道宽。','测墙到围栏的最窄净宽、凸柱及窗扇开启后的净宽。'),
'architecture':('建筑占位沿南北 25−7−8=10 m；东西进深暂7.9 m；高12.8 m。非实测建筑平面。','补首层凹凸与开口尺寸、实际建筑高度。'),
'paving':('红砖区按 7 × 4 m 区域校正；灰路宽1.6 m，位置暂定。砖尺寸与灰路细部未测。','补灰路边界、铺装坡度和拆池后砖面是否连续。')}
for k,(ass,res) in updates.items(): c['features'][k].update(assumption=ass,resolve=res)
c['features']['zone1']['title']='01 · 北侧主院'
c['features']['zone2']['title']='02 · 南侧次院'
for k in ['zone1','zone2']:c['features'][k]['confidence']='院宽已标注 / 局部定位暂定'
c['features']['boundary']['assumption']='围栏高暂1.35 m；北院入口按1.6 m通路关系示意，门叶约1.48 m；南门约1.1 m。门扇开启方向及实际净宽未核实。'
write('site-config.json',c)

# Each size is [height, spread] in metres. These are managed design envelopes,
# not promises of growth or botanical maximum size.
plants={
'OS':dict(name='桂花',en='Sweet osmanthus',botanical='Osmanthus fragrans',kind='tree',evergreen=True,color='#3e6240',mature='自然常达 3–6 m 或更高；本案控制高 3–4 m、冠幅 3–3.5 m',flower='约9–10月；品种、气温影响明显',light='日照至半日照；酷热暴晒处需水分保障',water='前两年根球保持均匀湿润；成活后旱热期深灌，忌积水',care='花后选择性疏枝；保留自然冠形，检查介壳虫。不是每年截顶的小球。',spacing=3.5,stock='高1.8–2.0 m，冠0.9–1.2 m，健康容器苗/土球苗',sizes={'1':[2,1.1],'3':[2.7,2.1],'5':[3.3,3]},bloom=['autumn'],source='https://plants.ces.ncsu.edu/plants/osmanthus-fragrans/'),
'CA':dict(name='白花茶梅',en='White sasanqua camellia',botanical='Camellia sasanqua',kind='shrub',evergreen=True,color='#355b42',mature='品种可达 2–4 m 以上；本案控制高 2–2.5 m、冠幅约2 m',flower='约11月至翌年2月，选定品种后细化；不是单株连续开花五个月',light='半阴、明亮散射光；避西晒和干冷风',water='中等；微酸性疏松土，保湿但不涝',care='花后轻疏，勿秋季齐剪花芽；巡查介壳虫、根腐及花腐。先测土壤pH。',spacing=2.1,stock='高0.9–1.2 m、冠0.6–0.8 m；本地露地越冬的白花苗',sizes={'1':[1.1,.75],'3':[1.7,1.35],'5':[2.2,1.95]},bloom=['winter'],source='https://plants.ces.ncsu.edu/plants/camellia-sasanqua/'),
'AB':dict(name='大花六道木',en='Glossy abelia',botanical='Abelia × grandiflora',kind='shrub',evergreen=False,color='#60804b',mature='普通类型高约1–2.5 m、冠1.5–2.5 m；本案疏枝控制在1.2–1.5 m',flower='约5–10月，零续开花',light='日照至半日照；太阴花少',water='中低；首年规律检查，成活后旱时补水',care='冬季可能落叶或冻梢，不能独担冬季隐私；早春疏老枝，保留拱垂形。',spacing=1.5,stock='高0.4–0.6 m、冠0.35–0.5 m，绿叶型',sizes={'1':[.6,.5],'3':[1.05,1.05],'5':[1.4,1.5]},bloom=['summer','autumn'],source='https://plants.ces.ncsu.edu/plants/abelia-x-grandiflora/'),
'HY':dict(name='白花大叶绣球',en='Bigleaf hydrangea',botanical='Hydrangea macrophylla',kind='shrub',evergreen=False,color='#65834c',mature='高、冠幅各约1–1.8 m；本案冠幅控制约1.2 m',flower='约5–7月，具体依品种',light='北院半阴；避下午热晒',water='中高；本案用量少，独立滴灌分区；不可常年涝根',care='老枝开花类型花后轻剪，冬季勿一律齐根剪；雨季通风，留意叶斑、白粉病。白花不承诺随pH变蓝。',spacing=1.4,stock='冠0.35–0.45 m，白花类型',sizes={'1':[.5,.45],'3':[.9,.95],'5':[1.2,1.2]},bloom=['summer'],source='https://plants.ces.ncsu.edu/plants/hydrangea-macrophylla/'),
'LI':dict(name='白花矮紫薇 Acoma',en="Acoma crape myrtle",botanical="Lagerstroemia 'Acoma'",kind='tree',evergreen=False,color='#61804f',mature='约3 m高、3–3.5 m冠幅；不同于7–10 m的大型紫薇品种',flower='约6–9月；盛花随天气变化',light='南院日照充足位置，先核实实际遮阴',water='中等；成活后耐短旱，热旱期深灌',care='选抗白粉病品种仍需通风；冬季只疏交叉枝，禁止“砍头”。Acoma本地库存尚未确认。',spacing=3.5,stock='高1.5–1.8 m、冠0.7–1 m，多干型',sizes={'1':[1.7,1],'3':[2.35,2],'5':[2.85,3.2]},bloom=['summer'],source='https://landscapeplants.oregonstate.edu/plants/lagerstroemia-acoma'),
'AS':dict(name='一叶兰',en='Cast-iron plant',botanical='Aspidistra elatior',kind='leaf',evergreen=True,color='#315f46',mature='高0.45–0.8 m，丛幅0.5–0.8 m',flower='花贴近地面，不作为观花配置',light='半阴至阴；不要放在无遮蔽的强直射阳光下',water='中低；首年保湿，成活后较耐旱，排水良好',care='剪老损叶，数年后拥挤才分株；避免强光灼伤与冬季干冷风。',spacing=.6,stock='每盆3–5片健康叶，15–20 cm容器',sizes={'1':[.4,.28],'3':[.55,.5],'5':[.65,.65]},bloom=[],source='https://plants.ces.ncsu.edu/plants/aspidistra-elatior/'),
'LM':dict(name='阔叶山麦冬',en='Big blue lilyturf',botanical='Liriope muscari',kind='grass',evergreen=True,color='#456c43',mature='高、丛幅约0.3–0.45 m',flower='约7–9月，紫色花穗',light='日照至半阴；深阴能活但生长、开花减弱',water='中低；第一年保湿，成活后旱时浇透，忌冠部积水',care='早春新叶萌发前可清理旧叶；3–5年拥挤时分株。采购丛生种，不误买蔓生近缘种。',spacing=.4,stock='10–12 cm容器苗，每丛3芽以上',sizes={'1':[.22,.2],'3':[.35,.36],'5':[.4,.44]},bloom=['summer'],source='https://plants.ces.ncsu.edu/plants/liriope-muscari/'),
'IT':dict(name='鸢尾',en='Roof iris',botanical='Iris tectorum',kind='iris',evergreen=False,color='#618265',mature='叶高0.3–0.45 m，花茎可稍高；丛幅约0.3–0.45 m',flower='约4–5月，淡紫',light='日照至半阴，通风，排水顺畅',water='中低；不可将陆生鸢尾当水生植物',care='根茎浅栽、勿厚埋；花后剪残梗，3年左右分株，检查蜗牛和烂根。冬季叶况随低温变化。',spacing=.4,stock='2–3芽健壮分株或容器苗',sizes={'1':[.25,.2],'3':[.4,.35],'5':[.42,.42]},bloom=['spring'],source='https://plants.ces.ncsu.edu/plants/iris-tectorum/'),
'TJ':dict(name='络石',en='Star jasmine',botanical='Trachelospermum jasminoides',kind='climber',evergreen=True,color='#3c6949',mature='未经管理可攀至6 m；本案限高1.8–2 m、单株宽约1.5 m',flower='约4–6月，白花',light='日照至半阴；阴处开花减少',water='中等；前两年规律检查，成活后旱时补水',care='仅牵引指定小段，花后及夏末整理；避开窗、百叶、管线；支撑及围栏抗风荷载须核实。',spacing=1.5,stock='藤长0.8–1 m、3 L以上容器苗',sizes={'1':[1,.45],'3':[1.8,1.15],'5':[1.9,1.5]},bloom=['spring'],source='https://plants.ces.ncsu.edu/plants/trachelospermum-jasminoides/'),
'ZJ':dict(name='结缕草',en='Japanese lawn grass',botanical='Zoysia japonica',kind='turf',evergreen=False,color='#849260',mature='草坪养护高度约3–5 cm；面积计量',flower='不作为观花植物',light='优先日照充足；先连续记录，目标至少约5–6小时直射光，非硬性保证',water='成坪前浅根区持续监测；成坪后旱时深灌，勿每日固定喷洒',care='生长季按1/3原则修剪，通常约7–14天检查一次；冬季休眠变稻草色，不冬播黑麦草。',spacing=0,stock='适季铺健康草皮，不是全年常绿草毯',sizes={'1':[.045,1],'3':[.045,1],'5':[.045,1]},bloom=[],source='https://content.ces.ncsu.edu/zoysiagrass-lawn-maintenance-calendar')}
write('plants.json',plants)

def row(x0,x1,z,step): return [[round(x,3),z] for x in sequence(x0,x1,step)]
def sequence(a,b,s):
 while a<=b+1e-7: yield a; a+=s
def grid(x0,x1,z0,z1,step):return [[round(x,3),round(z,3)] for z in sequence(z0,z1,step) for x in sequence(x0,x1,step)]
def area(poly):return abs(sum(poly[i][0]*poly[(i+1)%len(poly)][1]-poly[(i+1)%len(poly)][0]*poly[i][1] for i in range(len(poly))))/2
layouts={}
for opt in 'ABC':
 g=[];beds=[];paths=[];surfaces=[]
 def cohort(code,species,points,zone,base=0,note=''):
  g.append(dict(id=code,species=species,points=points,quantity=len(points),zone=zone,base=base,note=note))
 def patch(code,poly,kind='mulch'):
  surfaces.append(dict(id=code,polygon=poly,kind=kind,area=round(area(poly),2)))
 def path(code,points,width):paths.append(dict(id=code,points=points,width=width))
 if opt in 'AB':
  beds=['P1','P2'] if opt=='A' else ['P1']
  cohort('N01','LM',row(.8,4.8,.84,.4),1,.525,'P1东侧长列；池内净宽/排水待量，数量随实测调整')
  cohort('N02','IT',row(.8,4.8,1.28,.4),1,.525,'P1西侧长列；交错叶形，不混种十余品种')
  if opt=='A':
   cohort('N03','LM',row(.8,4.8,2.42,.4),1,.525)
   cohort('N04','IT',row(.8,4.8,2.86,.4),1,.525)
 else:
  patch('N-low-border',[[.35,.45],[5.15,.45],[5.15,3.45],[.35,3.45]])
  cohort('N01','CA',[[1.45,1.6],[3.6,1.6]],1,note='拆两池并局部起砖形成连通地栽花境；不是在砖上覆薄土')
  cohort('N02','LM',row(.7,4.7,2.95,.4),1)
  cohort('N03','IT',row(.7,4.7,2.5,.4),1)
 # Main composition, distinct from the raised bed band, viewed from north-facing house openings.
 patch('N-woodland',[[.3,4.25],[5.65,4.25],[5.7,5.75],[4.9,6.7],[1,6.7],[.3,6.2]])
 cohort('N10','CA',[[1.35,5],[3.5,5]],1,note='主院常绿骨架；五年冠幅约1.95 m')
 cohort('N11','HY',[[1.25,6.15],[2.9,6.15],[4.65,5.95]],1,note='仅三株，位于北院避热晒位置；保留疏松通风')
 cohort('N12','LM',row(.8,4.8,6.5,.4),1)
 patch('N-west-border',[[.3,8.75],[5.85,8.75],[5.85,9.8],[.3,9.8]])
 cohort('N13','LM',grid(.65,5.45,9.02,9.42,.4),1,note='灰路边低矮连续叶带，保持1.6 m通路')
 cohort('N14','TJ',[[2.1,9.78],[3.6,9.78]],1,note='西界仅3 m长分段屏风；高层俯视不能完全遮挡')
 # Keep louvres and outward-opening windows clear; no climber on the house.
 patch('E-shade-1',[[7.4,1.5],[9.75,1.5],[9.75,2],[7.4,2]])
 patch('E-shade-2',[[14.3,1.5],[16.45,1.5],[16.45,2],[14.3,2]])
 cohort('E01','LM',row(7.6,9.6,1.75,.4)+row(14.5,16.1,1.75,.4),3,note='低叶带延续两院；百叶前10–14 m区段留检修空地')
 # Aspidistra only in the shaded north wall corner, not exposed east planting strip.
 patch('N-wall-shade',[[5.75,4.2],[6.5,4.2],[6.5,6.25],[5.75,6.25]])
 cohort('N15','AS',[[6.05,4.6],[6.05,5.2],[6.05,5.8]],1,note='北墙散射光角落；距墙留检修带，实测窗扇后平移')
 if opt=='A':
  patch('S-lawn',[[19.6,2.5],[23.1,2.5],[23.1,5.65],[19.6,5.65]],'turf')
  path('S-main',[[17,6.3],[25,6.3]],1.2)
  path('S-side',[[18.15,.94],[18.15,6.3]],1.2)
  path('S-door',[[17,4.1],[18.15,4.1]],1.2)
 elif opt=='B':
  patch('S-lawn',[[20,2.5],[23.35,2.5],[23.65,3],[23.65,5.05],[23.1,5.5],[20.4,4.95],[20,4.45]],'turf')
  path('S-main',[[17,4.1],[18.8,4.1],[19.5,5.6],[22,6.3],[25,6.3]],1.2)
  path('S-side',[[18.15,.94],[18.3,2.8],[18.8,4.1]],1.2)
 else:
  patch('S-island',[[20.1,2.75],[22.8,2.75],[23.2,3.5],[23.1,4.65],[22.5,5],[20.4,4.6]],'mulch')
  path('S-loop',[[18.3,.94],[18.5,4.1],[19.7,6.3],[24.3,6.3],[24.1,2],[21,1.2],[18.3,.94]],1.15)
  path('S-door',[[17,4.1],[18.5,4.1]],1.2)
  path('S-gate',[[24.3,6.3],[25,6.3]],1.2)
  cohort('S10','AB',[[21,3.5],[22.5,3.6]],2)
  cohort('S11','LM',row(20.6,22.6,4.5,.4),2)
 patch('S-east-border',[[19.8,.2],[24.8,.2],[24.8,5.5],[23.8,5.5],[23.7,2.3],[20,2.2]])
 patch('S-west-border',[[17.8,7.45],[24.8,7.45],[24.8,9.8],[17.8,9.8]])
 # C shifts the east tree to maintain clearance to the loop's east segment.
 cohort('S01','OS',[[22.1,1.55]] if opt!='C' else [[21.5,3.7]],2,note='树冠在院内；先探管线、根域及土层，不植入封底水泥池')
 cohort('S02','LI',[[22,8.2]],2,note='夏花焦点；苗圃核对Acoma或成熟体量相当的白花抗病品种')
 cohort('S03','AB',[[24.05,3.05],[24.05,4.65]] if opt!='C' else [[19,8.55],[24,8.55]],2)
 if opt!='C':cohort('S04','AB',[[18.75,8.55],[20.25,8.55]],2)
 cohort('S05','IT',row(20.4,23.6,.55,.4),2)
 cohort('S06','LM',row(18.2,24.2,7.55,.4)+row(18.2,24.2,9.5,.4),2)
 cohort('S07','TJ',[[24.75,7.95],[24.75,9.25]],2,note='南侧西端2.8 m分段屏风，离院门和格栅口留空')
 # In C the island cannot contain both a small tree and overlapping medium shrubs.
 if opt=='C':
  g=[a for a in g if a['id']!='S10']
  cohort('S12','LM',grid(20.6,22.6,3.15,4.35,.4),2,note='无草坪方案，岛内低地被，围绕桂花留根颈空圈')
 # Continuous north approach connects brick apron to the gray entrance route.
 g=[a for a in g if a['species']!='AS']
 surfaces=[a for a in surfaces if a['id']!='N-wall-shade']
 path('N-connection',[[6.05,3.8],[6.05,7.8]],1.2)
 # Repeat the same groundcover in broad drifts; keep crowns and routes free.
 def in_poly(pt,poly):
  x,z=pt;inside=False
  for i in range(len(poly)):
   a,b=poly[i-1],poly[i]
   if (a[1]>z)!=(b[1]>z) and x<(b[0]-a[0])*(z-a[1])/(b[1]-a[1])+a[0]:inside=not inside
  return inside
 def dist_segment(p,a,b):
  dx,dz=b[0]-a[0],b[1]-a[1];den=dx*dx+dz*dz
  t=max(0,min(1,((p[0]-a[0])*dx+(p[1]-a[1])*dz)/den)) if den else 0
  return math.hypot(p[0]-a[0]-dx*t,p[1]-a[1]-dz*t)
 for code,surface,zone in [('N20','N-woodland',1),('S20','S-east-border',2),('S21','S-west-border',2)]+([('N21','N-low-border',1)] if opt=='C' else []):
  poly=next(a['polygon'] for a in surfaces if a['id']==surface);xs=[a[0] for a in poly];zs=[a[1] for a in poly];pts=[]
  for pt in grid(min(xs)+.22,max(xs)-.18,min(zs)+.22,max(zs)-.18,.4):
   if not in_poly(pt,poly):continue
   if any(dist_segment(pt,a,b)<pa['width']/2+.22 for pa in paths for a,b in zip(pa['points'],pa['points'][1:])):continue
   occupied=False
   for gg in g:
    radius=.48 if plants[gg['species']]['kind']=='tree' else .65 if plants[gg['species']]['kind']=='shrub' else .30
    if any(math.dist(pt,other)<radius for other in gg['points']):occupied=True;break
   if not occupied:pts.append(pt)
  if pts:cohort(code,'LM',pts,zone,note='成片重复的地被填充，保留木本根颈、通路与现有排水口；不以密植大灌木制造第一年效果')
 # Resolve mature groundcover edges against paths, grate service pad and tree root collars.
 treepts=[pt for gg in g if plants[gg['species']]['kind']=='tree' for pt in gg['points']]
 for gg in g:
  if plants[gg['species']]['kind'] not in ['grass','iris']:continue
  gg['points']=[pt for pt in gg['points'] if not (23.23<pt[0]<24.62 and 6.2<pt[1]<7.62) and not any(math.dist(pt,t)<.38 for t in treepts) and not any(dist_segment(pt,a,b)<pa['width']/2+.20 for pa in paths for a,b in zip(pa['points'],pa['points'][1:]))]
  gg['quantity']=len(gg['points'])
 g=[gg for gg in g if gg['quantity']]
 # Groundcover cells are explicit, and therefore quantities match the 3D scene.
 totals={}
 for a in g:totals[a['species']]=totals.get(a['species'],0)+a['quantity']
 for s in surfaces:
  if s['kind']=='turf':totals['ZJ']=s['area']
 layouts[opt]=dict(id=opt,title={'A':'双池 · 平行花带','B':'一池 · 林缘与开敞草坪','C':'无池 · 连续花境与环路'}[opt],retainedBeds=beds,groups=g,surfaces=surfaces,paths=paths,quantities=totals,recommended=opt=='B')
write('layouts.json',layouts)
print('Calibrated R1; planting totals:',{k:v['quantities'] for k,v in layouts.items()})
