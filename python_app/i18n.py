# -*- coding: utf-8 -*-
"""Тексты интерфейса на трёх языках: ru, en, zh."""

def F(num, den):
    """Дробь num/den; разметку <frac> разбирает htmlview."""
    return '<frac>' + num + '\x01' + den + '</frac>'


ru = {
    # меню «Цвета» и легенда под сосудом
    'colorsMenu': 'Цвета',
    'zoomLabel': 'масштаб',
    'zoomAll': 'вся шкала 0…N',
    'colMolTitle': 'Молекулы',
    'colMolRegion': 'в области / вне области',
    'colMolSpeed': 'по скорости',
    'colMolOrigin': 'по начальному положению',
    'colHistTitle': 'Гистограмма',
    'colHistOne': 'одним цветом',
    'colHistSigma': 'по отклонению от ⟨n⟩ (σ, 2σ)',
    'colSchemeTitle': 'Цветовая схема',
    'colScheme_color': 'цветная',
    'colScheme_contrast': 'контрастная (для проектора)',
    'colScheme_bw': 'чёрно-белая (для печати и цитирования)',
    'legIn': 'в области v',
    'legOut': 'вне области',
    'legImp': 'примесь',
    'legTag': '«Самая-Самая»',
    'legSpeed': 'медленные → быстрые',
    'legStartIn': 'начали в области',
    'legStartOut': 'начали снаружи',
    'tocExtra': 'Форма области и молекулы',
    'preset112': 'Две молекулы: вероятности P(0), P(1), P(2) (задача 1.12)',
    'presetBinom': 'Биномиальное распределение: область — половина сосуда',
    'presetPoisson': 'Маленькая область в большом сосуде → распределение Пуассона',
    'preset33': 'Область почти во весь сосуд: Пуассон для N − n (задача 3.3)',
    'presetHole': 'Заполнение области через отверстие: релаксация к равновесию',
    'presetDense': 'Плотный газ: флуктуации меньше биномиальных',
    'presetImp': 'Газ с примесью крупных молекул',
    'presetCorner': 'Закрашенная область в углу сосуда, как на рисунке задачи',
    'presetBigV': 'Сосуд вдвое больше при той же области (меняем V)',
    'presetDiatomic': 'Атомы объединены в двухатомные молекулы',
    'presetBigAtoms': 'Атомы большого размера (исключённый объём)',
    'presetFew': 'Несколько молекул: дискретность распределения',
    'secVessel': 'Сосуд и область',
    'Wv': 'Ширина сосуда (объём V)',
    'shape': 'Форма выделенной области',
    'shapeStrip': 'полоса у левой стенки',
    'shapeCorner': 'прямоугольник в углу',
    'diatomic': 'Объединить атомы в двухатомные молекулы',
    'hole': 'Размер отверстия (доля стороны области)',
    'pairsNote': 'n — число атомов; теория: молекулы по 2 атома',
    'frac': 'Доля объёма сосуда v/V',
    'theoryExtra': '<h2 id="t11">11. Форма области, объём сосуда и двухатомные молекулы</h2><p>Распределение числа молекул зависит только от отношения площадей <i>p</i> = <i>v</i>/<i>V</i>, но не от формы выделенной области: в программе её можно сделать полосой у стенки или прямоугольником в углу сосуда, как на рисунке к задаче. Если увеличить сосуд при неизменной области, <i>p</i> уменьшается, ⟨<i>n</i>⟩ = <i>Np</i> падает, а относительная флуктуация растёт.</p><p>Если атомы попарно объединены в двухатомные молекулы, в область входят и выходят сразу по два атома. Число молекул <i>k</i> в области распределено биномиально с параметрами <i>N</i>/2 и <i>p</i>, а число атомов <i>n</i> ≈ 2<i>k</i>, поэтому</p><div class="eq">⟨n⟩ = Np,&nbsp;&nbsp; σ² ≈ 4·' + F('N', '2') + '·p(1 − p) = 2Np(1 − p),</div><p>т. е. среднее не меняется, а дисперсия удваивается (задача 2.14). На гистограмме преобладают чётные значения <i>n</i>.</p>',
    'langName': 'Русский',
    'appTitle': 'Частицы в выделенном объёме',
    'kicker': 'Статистическая физика · интерактивная демонстрация',
    'appSubtitle': 'Флуктуации числа молекул идеального газа в мысленно выделенной области сосуда: распределения Бернулли, биномиальное и Пуассона, марковская динамика.',
    'menuDemo': 'Демонстрация',
    'menuTheory': 'Теоретическая часть',
    'menuAuthors': 'Авторы',
    'menuLanguage': 'Язык',
    'back': '← Меню',
    'play': '▶ Пуск',
    'pause': '⏸ Пауза',
    'reset': '⟲ Заново',
    'clearStats': 'Сбросить статистику',
    'secStats': 'Статистика',
    'secPresets': 'Готовые опыты',
    'presetNone': '— выберите опыт —',
    'secParticles': 'Молекулы',
    'N': 'Число молекул N',
    'r': 'Радиус молекулы r',
    'u': 'Температура (тепловая скорость)',
    'secVolume': 'Выделенный объём',
    'secWall': 'Перегородка',
    'wall': 'Непроницаемая стенка на границе объёма',
    'secImp': 'Примесь',
    'impN': 'Число молекул примеси',
    'impR': 'Радиус молекул примеси',
    'count': 'Считать в объёме',
    'countMain': 'основные молекулы',
    'countImp': 'молекулы примеси',
    'countAll': 'все молекулы',
    'secSim': 'Моделирование',
    'speed': 'Скорость моделирования',
    'init': 'Начальное состояние',
    'initUniform': 'равномерное',
    'initOutside': 'все снаружи объёма',
    'initInside': 'все внутри объёма',
    'tagged': 'Выделить одну молекулу («Самая-Самая»)',
    'showBinom': 'биномиальное',
    'showPois': 'Пуассон',
    'showGauss': 'Гаусс',
    'vesselTitle': 'Сосуд',
    'histTitle': 'Распределение вероятностей P(n)',
    'timeTitle': 'Временная динамика n(t)',
    'legExp': 'эксперимент',
    'legBinom': 'биномиальное',
    'legPois': 'Пуассон',
    'legPoisMirror': 'Пуассон для N − n',
    'legGauss': 'Гаусс',
    'legMean': '⟨n⟩ ± σ (теория)',
    'axisN': 'n',
    'axisP': 'P(n)',
    'axisT': 't, усл. ед.',
    'axisNt': 'n(t)',
    'noData': 'Нажмите «Пуск», чтобы набрать статистику',
    'closedNote': 'Отверстие меньше диаметра молекулы — стенка непроницаема, число молекул в объёме сохраняется',
    'stN': 'Сейчас в объёме n',
    'stSamples': 'Число выборок',
    'stP': 'p = v/V (доступная площадь)',
    'stMean': 'Среднее ⟨n⟩',
    'stVar': 'Дисперсия σ²',
    'stRel': 'Относительная флуктуация σ/⟨n⟩',
    'stTag': 'Доля времени выделенной молекулы в объёме',
    'colExp': 'опыт',
    'colTheory': 'теория',
    # страница авторов
    'authUniv': 'Московский государственный университет имени М. В. Ломоносова',
    'authFaculty': 'Факультет вычислительной математики и кибернетики',
    'author1': 'Кирсберг Арина Павловна',
    'author2': 'Черяпина Анна Сергеевна',
    'authSupervisor': 'Руководитель: Чичигина Ольга Александровна',
    'authLecturer': 'Лектор: Григорьев Кирилл Сергеевич',
    'tocRefs': 'Литература',
    'theoryRefs': '<h2 id="t12">Литература</h2><p>О. А. Чичигина. <i>Вероятностные распределения физических величин. Сборник задач.</i> — М.: Физический факультет МГУ, 2026. Задачи 1.10–1.12, 2.13–2.16, 2.23, 3.3.</p>',
    'theoryHtml': (
      '<nav class="toc"><a href="#t1">Модель</a><a href="#t2">Бернулли</a><a href="#t3">Биномиальное</a><a href="#t4">Пуассон</a><a href="#t5">Гаусс</a><a href="#t6">v ≈ V</a><a href="#t7">Марковский процесс</a><a href="#t8">Отверстие</a><a href="#t9">Размер и примесь</a><a href="#t10">Задачи</a></nav>' +
      '<h2 id="t1">1. Модель</h2>' +
      '<p>Рассматривается двумерная модель идеального газа: <i>N</i> молекул движутся в сосуде площадью <i>V</i> (длина <i>a</i>, ширина <i>b</i>), упруго сталкиваясь друг с другом и со стенками. В сосуде мысленно выделена область площадью <i>v</i> (на экране она закрашена). Число молекул <i>n</i>, оказавшихся в ней в данный момент, — <b>дискретная случайная величина</b>, принимающая значения 0, 1, …, <i>N</i>.</p>' +
      '<p>На экране молекулы внутри выделенной области закрашены, снаружи — полые, как на рисунке к задаче 2.14.</p>' +
      '<h2 id="t2">2. Одна молекула: распределение Бернулли</h2>' +
      '<p>В равновесии молекула с одинаковой вероятностью может оказаться в любой точке сосуда, поэтому вероятность обнаружить её в выделенной области равна отношению площадей:</p>' +
      '<div class="eq">p = ' + F('v', 'V') + ',&nbsp;&nbsp; q = 1 − p.</div>' +
      '<p>Величина <i>n</i><sub>1</sub> = 1 (молекула внутри) или 0 (снаружи) распределена по Бернулли: ⟨<i>n</i><sub>1</sub>⟩ = <i>p</i>, σ² = <i>p</i>(1 − <i>p</i>). Включите «Выделить одну молекулу» — доля времени, проведённого ею в объёме, стремится к <i>p</i> (задачи 1.10 п.1, 2.13).</p>' +
      '<h2 id="t3">3. N молекул: биномиальное распределение</h2>' +
      '<p>Молекулы идеального газа не взаимодействуют, поэтому попадания разных молекул в область независимы, а <i>n</i> — сумма <i>N</i> независимых величин Бернулли:</p>' +
      '<div class="eq">P<sub>N</sub>(n) = ' + F('N!', 'n!(N − n)!') + ' p<sup>n</sup>(1 − p)<sup>N−n</sup>,</div>' +
      '<div class="eq">⟨n⟩ = Np,&nbsp;&nbsp; σ² = Np(1 − p),&nbsp;&nbsp; ' + F('σ', '⟨n⟩') + ' = √' + F('1 − p', 'Np') + '.</div>' +
      '<p>Относительная флуктуация убывает как 1/√<i>N</i> — поэтому макроскопическая плотность газа практически не флуктуирует. Распределение двухпараметрическое (<i>N</i>, <i>p</i>).</p>' +
      '<p><b>Пример (задача 1.12).</b> <i>N</i> = 2, <i>p</i> = 0.1. Перебор: оба снаружи — 0.9·0.9 = 0.81; одна внутри — 2·0.1·0.9 = 0.18; обе внутри — 0.01. Сумма 1 — нормировка выполнена.</p>' +
      '<h2 id="t4">4. Предел Пуассона</h2>' +
      '<p>Если <i>N</i> → ∞, <i>p</i> → 0, а <i>Np</i> = λ = const (малый объём в большом сосуде, <i>v</i> ≪ <i>V</i>), то, заменяя <i>p</i> = λ/<i>N</i> и используя второй замечательный предел (задача 2.23):</p>' +
      '<div class="eq">P(n) = ' + F('λ<sup>n</sup>', 'n!') + ' e<sup>−λ</sup>,&nbsp;&nbsp; ⟨n⟩ = σ² = λ = n<sub>0</sub>v,</div>' +
      '<p>где <i>n</i><sub>0</sub> = <i>N</i>/<i>V</i> — концентрация. Распределение однопараметрическое и зависит только от концентрации и размера выделенного объёма, но не от размера сосуда (задача 2.16).</p>' +
      '<h2 id="t5">5. Предел Гаусса</h2>' +
      '<p>При <i>Np</i>(1 − <i>p</i>) ≫ 1 биномиальное распределение переходит в нормальное (задача 3.12):</p>' +
      '<div class="eq">P(n) ≈ ' + F('1', '√(2πσ²)') + ' exp[ −' + F('(n − Np)²', '2σ²') + ' ],&nbsp;&nbsp; σ² = Np(1 − p).</div>' +
      '<h2 id="t6">6. Объём, близкий к полному (задача 3.3)</h2>' +
      '<p>Условия <i>n</i> ≫ 1 недостаточно для перехода к непрерывному описанию. Если <i>v</i> немного меньше <i>V</i>, то <i>n</i> принимает лишь несколько значений <i>N</i>, <i>N</i> − 1, <i>N</i> − 2, … Малым является число молекул <i>m</i> = <i>N</i> − <i>n</i> <b>вне</b> области, и оно распределено по Пуассону:</p>' +
      '<div class="eq">P(n) = ' + F('λ<sup>N−n</sup> e<sup>−λ</sup>', '(N − n)!') + ',&nbsp;&nbsp; λ = N(1 − p).</div>' +
      '<p>При <i>p</i> > 0.5 программа рисует именно такую «отражённую» кривую Пуассона.</p>' +
      '<h2 id="t7">7. Временная динамика: дискретный марковский процесс</h2>' +
      '<p>Выделенная молекула то входит в область, то выходит из неё (телеграфный сигнал). Если за время пребывания она успевает много раз столкнуться и «забыть» прошлое, времена пребывания внутри <i>t</i><sub>1</sub> и снаружи <i>t</i><sub>2</sub> распределены экспоненциально, а вероятности перехода в единицу времени постоянны: γ<sub>−</sub> = 1/⟨<i>t</i><sub>1</sub>⟩ (выход), γ<sub>+</sub> = 1/⟨<i>t</i><sub>2</sub>⟩ (вход). Тогда</p>' +
      '<div class="eq">p = ' + F('⟨t<sub>1</sub>⟩', '⟨t<sub>1</sub>⟩ + ⟨t<sub>2</sub>⟩') + ' = ' + F('γ<sub>+</sub>', 'γ<sub>+</sub> + γ<sub>−</sub>') + '.</div>' +
      '<p>Число молекул <i>n</i> совершает процесс рождения–гибели: <i>n</i> → <i>n</i> + 1 с интенсивностью (<i>N</i> − <i>n</i>)γ<sub>+</sub>, <i>n</i> → <i>n</i> − 1 с интенсивностью <i>n</i>γ<sub>−</sub>. Основное кинетическое уравнение:</p>' +
      '<div class="eq">' + F('dP<sub>n</sub>', 'dt') + ' = (N − n + 1)γ<sub>+</sub>P<sub>n−1</sub> + (n + 1)γ<sub>−</sub>P<sub>n+1</sub> − [(N − n)γ<sub>+</sub> + nγ<sub>−</sub>]P<sub>n</sub>.</div>' +
      '<p>Его стационарное решение — биномиальное распределение. Среднее релаксирует экспоненциально:</p>' +
      '<div class="eq">⟨n⟩(t) = Np + (n(0) − Np) e<sup>−t/τ</sup>,&nbsp;&nbsp; 1/τ = γ<sub>+</sub> + γ<sub>−</sub>.</div>' +
      '<p>Выберите начальное состояние «все снаружи объёма» и наблюдайте релаксацию на графике <i>n</i>(<i>t</i>).</p>' +
      '<h2 id="t8">8. Перегородка с отверстием</h2>' +
      '<p>Пусть область отделена стенкой с отверстием длиной <i>c</i>. В двумерном газе поток молекул через отверстие</p>' +
      '<div class="eq">J = ' + F('n<sub>s</sub> ⟨|v|⟩ c', 'π') + ',</div>' +
      '<p>где <i>n</i><sub>s</sub> — концентрация, ⟨|<i>v</i>|⟩ ∝ √<i>T</i> — средняя скорость. Поэтому уменьшение отверстия и понижение температуры <b>замедляют</b> обмен молекулами (растёт τ и время корреляции <i>n</i>(<i>t</i>)), но <b>не меняют</b> равновесное распределение: оно остаётся биномиальным с <i>p</i> = <i>v</i>/<i>V</i>. Если отверстие меньше диаметра молекулы, стенка непроницаема и <i>n</i> = const — распределение становится детерминированным (δ-функция).</p>' +
      '<h2 id="t9">9. Конечный размер молекул и примесь</h2>' +
      '<p>Модель идеального газа предполагает точечные частицы. У дисков радиуса <i>r</i> центр не может подойти к стенке ближе <i>r</i>, поэтому программа вычисляет <i>p</i> по доступной площади. Кроме того, диски не перекрываются (исключённый объём) — появляются корреляции, и при большой плотности флуктуации становятся <b>меньше</b> биномиальных (задача 2.14, п. 6). Примесь крупных молекул занимает часть объёма и дополнительно «толкается» с основными молекулами; можно исследовать распределение числа молекул каждой компоненты в отдельности.</p>' +
      '<h2 id="t10">10. Задачи из пособия и как проверить их в демонстрации</h2>' +
      '<table class="tasks"><tr><th>№</th><th>Задача</th><th>Опыт в программе</th></tr>' +
      '<tr><td>1.10</td><td>Бернулли для газа: величина, равная 1, если выделенная молекула в объёме; число частиц в объёме при <i>N</i> = 1.</td><td>Включите выделенную молекулу; поставьте <i>N</i> = 1 и сравните гистограмму с распределением Бернулли.</td></tr>' +
      '<tr><td>1.11</td><td>Диалог частиц в объёме с закутком.</td><td>Понаблюдайте за выделенной молекулой: сколько она проводит внутри, как часто входит и выходит.</td></tr>' +
      '<tr><td>1.12</td><td>Две частицы в закутке, <i>p</i> = 0.1: перебор и биномиальное распределение.</td><td>Опыт «Задача 1.12». Ожидается P(0) = 0.81, P(1) = 0.18, P(2) = 0.01.</td></tr>' +
      '<tr><td>2.13</td><td>Приключения Самой-Самой: вероятности событий для выделенной молекулы.</td><td>Доля времени выделенной молекулы в объёме → <i>v</i>/<i>V</i>.</td></tr>' +
      '<tr><td>2.14</td><td>Молекулы в закутке: какие из М, Д, Э не меняются при переносе объёма, изменении <i>N</i> и <i>V</i>, объединении в молекулы, увеличении размера атомов.</td><td>Меняйте <i>N</i>, долю объёма, радиус, включайте плотный газ; сравнивайте среднее и дисперсию.</td></tr>' +
      '<tr><td>2.15</td><td>Как именно изменится характеристика (во сколько раз).</td><td>Удвойте <i>N</i>: среднее и дисперсия удваиваются, σ/⟨<i>n</i>⟩ уменьшается в √2 раз.</td></tr>' +
      '<tr><td>2.16</td><td>Биномиальное против Пуассона.</td><td>Включите обе кривые и сравните их при разных <i>v</i>/<i>V</i>.</td></tr>' +
      '<tr><td>2.23</td><td>От биномиального к Пуассону: <i>N</i> → ∞, <i>p</i> → 0, <i>Np</i> = const.</td><td>Опыт «Предел Пуассона»; увеличивайте <i>N</i>, уменьшая <i>v</i>/<i>V</i>.</td></tr>' +
      '<tr><td>3.3</td><td>Объём, немного меньший полного: пуассоновское распределение для частиц в оставшейся части.</td><td>Опыт «Задача 3.3», кривая «Пуассон для <i>N</i> − <i>n</i>».</td></tr>' +
      '</table>')
}

  
en = {
    # меню «Цвета» и легенда под сосудом
    'colorsMenu': 'Colors',
    'zoomLabel': 'scale',
    'zoomAll': 'full range 0…N',
    'colMolTitle': 'Molecules',
    'colMolRegion': 'inside / outside the region',
    'colMolSpeed': 'by speed',
    'colMolOrigin': 'by starting position',
    'colHistTitle': 'Histogram',
    'colHistOne': 'single color',
    'colHistSigma': 'by deviation from ⟨n⟩ (σ, 2σ)',
    'colSchemeTitle': 'Color scheme',
    'colScheme_color': 'color',
    'colScheme_contrast': 'high contrast (projector)',
    'colScheme_bw': 'black and white (print, citing)',
    'legIn': 'in region v',
    'legOut': 'outside',
    'legImp': 'impurity',
    'legTag': '"The Very One"',
    'legSpeed': 'slow → fast',
    'legStartIn': 'started inside',
    'legStartOut': 'started outside',
    'tocExtra': 'Region shape and molecules',
    'preset112': 'Two molecules: probabilities P(0), P(1), P(2) (problem 1.12)',
    'presetBinom': 'Binomial distribution: the region is half of the vessel',
    'presetPoisson': 'Small region in a large vessel → Poisson distribution',
    'preset33': 'Region almost the whole vessel: Poisson for N − n (problem 3.3)',
    'presetHole': 'Filling the region through a hole: relaxation to equilibrium',
    'presetDense': 'Dense gas: fluctuations smaller than binomial',
    'presetImp': 'Gas with an impurity of large molecules',
    'presetCorner': 'Shaded region in the vessel corner, as in the problem figure',
    'presetBigV': 'Vessel twice as large, same region (changing V)',
    'presetDiatomic': 'Atoms joined into diatomic molecules',
    'presetBigAtoms': 'Large atoms (excluded volume)',
    'presetFew': 'A few molecules: discreteness of the distribution',
    'secVessel': 'Vessel and region',
    'Wv': 'Vessel width (volume V)',
    'shape': 'Shape of the selected region',
    'shapeStrip': 'strip at the left wall',
    'shapeCorner': 'rectangle in the corner',
    'diatomic': 'Join atoms into diatomic molecules',
    'hole': 'Hole size (fraction of the region side)',
    'pairsNote': 'n is the number of atoms; theory: molecules of 2 atoms',
    'frac': 'Fraction of the vessel volume v/V',
    'theoryExtra': '<h2 id="t11">11. Region shape, vessel volume and diatomic molecules</h2><p>The distribution of the number of molecules depends only on the area ratio <i>p</i> = <i>v</i>/<i>V</i>, not on the shape of the region: in the program it can be a strip at the wall or a rectangle in the corner of the vessel, as in the problem figure. Enlarging the vessel with the region fixed decreases <i>p</i> and ⟨<i>n</i>⟩ = <i>Np</i>, while the relative fluctuation grows.</p><p>If atoms are joined pairwise into diatomic molecules, they enter and leave the region two at a time. The number of molecules <i>k</i> in the region is binomial with parameters <i>N</i>/2 and <i>p</i>, and the number of atoms is <i>n</i> ≈ 2<i>k</i>, hence</p><div class="eq">⟨n⟩ = Np,&nbsp;&nbsp; σ² ≈ 4·' + F('N', '2') + '·p(1 − p) = 2Np(1 − p),</div><p>so the mean is unchanged while the variance doubles (problem 2.14). Even values of <i>n</i> dominate the histogram.</p>',
    'langName': 'English',
    'appTitle': 'Particles in a Selected Volume',
    'kicker': 'Statistical physics · interactive demonstration',
    'appSubtitle': 'Fluctuations of the number of ideal-gas molecules in a mentally selected part of a vessel: Bernoulli, binomial and Poisson distributions, Markov dynamics.',
    'menuDemo': 'Demonstration',
    'menuTheory': 'Theory',
    'menuAuthors': 'Authors',
    'menuLanguage': 'Language',
    'back': '← Menu',
    'play': '▶ Run',
    'pause': '⏸ Pause',
    'reset': '⟲ Restart',
    'clearStats': 'Clear statistics',
    'secStats': 'Statistics',
    'secPresets': 'Ready-made experiments',
    'presetNone': '— choose an experiment —',
    'secParticles': 'Molecules',
    'N': 'Number of molecules N',
    'r': 'Molecule radius r',
    'u': 'Temperature (thermal speed)',
    'secVolume': 'Selected volume',
    'secWall': 'Partition',
    'wall': 'Impermeable wall at the volume boundary',
    'secImp': 'Impurity',
    'impN': 'Number of impurity molecules',
    'impR': 'Impurity molecule radius',
    'count': 'Count in the volume',
    'countMain': 'main molecules',
    'countImp': 'impurity molecules',
    'countAll': 'all molecules',
    'secSim': 'Simulation',
    'speed': 'Simulation speed',
    'init': 'Initial state',
    'initUniform': 'uniform',
    'initOutside': 'all outside the volume',
    'initInside': 'all inside the volume',
    'tagged': 'Tag one molecule ("The Very One")',
    'showBinom': 'binomial',
    'showPois': 'Poisson',
    'showGauss': 'Gauss',
    'vesselTitle': 'Vessel',
    'histTitle': 'Probability distribution P(n)',
    'timeTitle': 'Time dynamics n(t)',
    'legExp': 'experiment',
    'legBinom': 'binomial',
    'legPois': 'Poisson',
    'legPoisMirror': 'Poisson for N − n',
    'legGauss': 'Gauss',
    'legMean': '⟨n⟩ ± σ (theory)',
    'axisN': 'n',
    'axisP': 'P(n)',
    'axisT': 't, arb. units',
    'axisNt': 'n(t)',
    'noData': 'Press "Run" to collect statistics',
    'closedNote': 'The hole is smaller than a molecule diameter — the wall is impermeable, the number of molecules in the volume is conserved',
    'stN': 'Now in the volume n',
    'stSamples': 'Number of samples',
    'stP': 'p = v/V (accessible area)',
    'stMean': 'Mean ⟨n⟩',
    'stVar': 'Variance σ²',
    'stRel': 'Relative fluctuation σ/⟨n⟩',
    'stTag': 'Fraction of time the tagged molecule is inside',
    'colExp': 'experiment',
    'colTheory': 'theory',
    # страница авторов
    'authUniv': 'Lomonosov Moscow State University',
    'authFaculty': 'Faculty of Computational Mathematics and Cybernetics',
    'author1': 'Arina Pavlovna Kirsberg',
    'author2': 'Anna Sergeevna Cheryapina',
    'authSupervisor': 'Supervisor: Olga Aleksandrovna Chichigina',
    'authLecturer': 'Lecturer: Kirill Sergeevich Grigoriev',
    'tocRefs': 'References',
    'theoryRefs': '<h2 id="t12">References</h2><p>O. A. Chichigina. <i>Probability Distributions of Physical Quantities. Problem Book.</i> Moscow: Faculty of Physics, MSU, 2026. Problems 1.10–1.12, 2.13–2.16, 2.23, 3.3.</p>',
    'theoryHtml': (
      '<nav class="toc"><a href="#t1">Model</a><a href="#t2">Bernoulli</a><a href="#t3">Binomial</a><a href="#t4">Poisson</a><a href="#t5">Gauss</a><a href="#t6">v ≈ V</a><a href="#t7">Markov process</a><a href="#t8">Hole</a><a href="#t9">Size and impurity</a><a href="#t10">Problems</a></nav>' +
      '<h2 id="t1">1. Model</h2>' +
      '<p>We consider a two-dimensional model of an ideal gas: <i>N</i> molecules move in a vessel of area <i>V</i> (length <i>a</i>, width <i>b</i>), colliding elastically with each other and with the walls. A region of area <i>v</i> is mentally selected in the vessel (shaded on screen). The number <i>n</i> of molecules found in it at a given moment is a <b>discrete random variable</b> taking the values 0, 1, …, <i>N</i>.</p>' +
      '<p>On screen, molecules inside the selected region are filled and those outside are hollow, as in the figure for problem 2.14.</p>' +
      '<h2 id="t2">2. One molecule: the Bernoulli distribution</h2>' +
      '<p>In equilibrium a molecule is equally likely to be at any point of the vessel, so the probability of finding it in the selected region equals the ratio of areas:</p>' +
      '<div class="eq">p = ' + F('v', 'V') + ',&nbsp;&nbsp; q = 1 − p.</div>' +
      '<p>The variable <i>n</i><sub>1</sub> = 1 (inside) or 0 (outside) is Bernoulli distributed: ⟨<i>n</i><sub>1</sub>⟩ = <i>p</i>, σ² = <i>p</i>(1 − <i>p</i>). Turn on "Tag one molecule": the fraction of time it spends in the volume tends to <i>p</i> (problems 1.10 item 1, 2.13).</p>' +
      '<h2 id="t3">3. N molecules: the binomial distribution</h2>' +
      '<p>Ideal-gas molecules do not interact, so the events "molecule is inside" are independent for different molecules and <i>n</i> is a sum of <i>N</i> independent Bernoulli variables:</p>' +
      '<div class="eq">P<sub>N</sub>(n) = ' + F('N!', 'n!(N − n)!') + ' p<sup>n</sup>(1 − p)<sup>N−n</sup>,</div>' +
      '<div class="eq">⟨n⟩ = Np,&nbsp;&nbsp; σ² = Np(1 − p),&nbsp;&nbsp; ' + F('σ', '⟨n⟩') + ' = √' + F('1 − p', 'Np') + '.</div>' +
      '<p>The relative fluctuation decreases as 1/√<i>N</i>, which is why the macroscopic density of a gas practically does not fluctuate. The distribution has two parameters (<i>N</i>, <i>p</i>).</p>' +
      '<p><b>Example (problem 1.12).</b> <i>N</i> = 2, <i>p</i> = 0.1. By enumeration: both outside 0.9·0.9 = 0.81; one inside 2·0.1·0.9 = 0.18; both inside 0.01. The sum is 1, so the distribution is normalized.</p>' +
      '<h2 id="t4">4. The Poisson limit</h2>' +
      '<p>If <i>N</i> → ∞, <i>p</i> → 0 with <i>Np</i> = λ = const (a small volume in a large vessel, <i>v</i> ≪ <i>V</i>), then substituting <i>p</i> = λ/<i>N</i> and using the second remarkable limit (problem 2.23):</p>' +
      '<div class="eq">P(n) = ' + F('λ<sup>n</sup>', 'n!') + ' e<sup>−λ</sup>,&nbsp;&nbsp; ⟨n⟩ = σ² = λ = n<sub>0</sub>v,</div>' +
      '<p>where <i>n</i><sub>0</sub> = <i>N</i>/<i>V</i> is the concentration. The distribution has one parameter and depends only on the concentration and the size of the selected volume, not on the vessel size (problem 2.16).</p>' +
      '<h2 id="t5">5. The Gaussian limit</h2>' +
      '<p>For <i>Np</i>(1 − <i>p</i>) ≫ 1 the binomial distribution becomes normal (problem 3.12):</p>' +
      '<div class="eq">P(n) ≈ ' + F('1', '√(2πσ²)') + ' exp[ −' + F('(n − Np)²', '2σ²') + ' ],&nbsp;&nbsp; σ² = Np(1 − p).</div>' +
      '<h2 id="t6">6. Volume close to the whole vessel (problem 3.3)</h2>' +
      '<p>The condition <i>n</i> ≫ 1 is not enough to switch to a continuous description. If <i>v</i> is slightly smaller than <i>V</i>, <i>n</i> takes only a few values <i>N</i>, <i>N</i> − 1, <i>N</i> − 2, … The small quantity is the number <i>m</i> = <i>N</i> − <i>n</i> of molecules <b>outside</b> the region, and it is Poisson distributed:</p>' +
      '<div class="eq">P(n) = ' + F('λ<sup>N−n</sup> e<sup>−λ</sup>', '(N − n)!') + ',&nbsp;&nbsp; λ = N(1 − p).</div>' +
      '<p>For <i>p</i> > 0.5 the program draws exactly this "mirrored" Poisson curve.</p>' +
      '<h2 id="t7">7. Time dynamics: a discrete Markov process</h2>' +
      '<p>The tagged molecule keeps entering and leaving the region (a telegraph signal). If during each stay it collides many times and "forgets" its past, the residence times inside <i>t</i><sub>1</sub> and outside <i>t</i><sub>2</sub> are exponentially distributed and the transition probabilities per unit time are constant: γ<sub>−</sub> = 1/⟨<i>t</i><sub>1</sub>⟩ (exit), γ<sub>+</sub> = 1/⟨<i>t</i><sub>2</sub>⟩ (entry). Then</p>' +
      '<div class="eq">p = ' + F('⟨t<sub>1</sub>⟩', '⟨t<sub>1</sub>⟩ + ⟨t<sub>2</sub>⟩') + ' = ' + F('γ<sub>+</sub>', 'γ<sub>+</sub> + γ<sub>−</sub>') + '.</div>' +
      '<p>The number <i>n</i> performs a birth–death process: <i>n</i> → <i>n</i> + 1 with rate (<i>N</i> − <i>n</i>)γ<sub>+</sub>, <i>n</i> → <i>n</i> − 1 with rate <i>n</i>γ<sub>−</sub>. The master equation is</p>' +
      '<div class="eq">' + F('dP<sub>n</sub>', 'dt') + ' = (N − n + 1)γ<sub>+</sub>P<sub>n−1</sub> + (n + 1)γ<sub>−</sub>P<sub>n+1</sub> − [(N − n)γ<sub>+</sub> + nγ<sub>−</sub>]P<sub>n</sub>.</div>' +
      '<p>Its stationary solution is the binomial distribution. The mean relaxes exponentially:</p>' +
      '<div class="eq">⟨n⟩(t) = Np + (n(0) − Np) e<sup>−t/τ</sup>,&nbsp;&nbsp; 1/τ = γ<sub>+</sub> + γ<sub>−</sub>.</div>' +
      '<p>Choose the initial state "all outside the volume" and watch the relaxation on the <i>n</i>(<i>t</i>) plot.</p>' +
      '<h2 id="t8">8. Partition with a hole</h2>' +
      '<p>Let the region be separated by a wall with a hole of length <i>c</i>. In a two-dimensional gas the flux of molecules through the hole is</p>' +
      '<div class="eq">J = ' + F('n<sub>s</sub> ⟨|v|⟩ c', 'π') + ',</div>' +
      '<p>where <i>n</i><sub>s</sub> is the concentration and ⟨|<i>v</i>|⟩ ∝ √<i>T</i> is the mean speed. So a smaller hole or a lower temperature <b>slows down</b> the exchange of molecules (τ and the correlation time of <i>n</i>(<i>t</i>) grow) but <b>does not change</b> the equilibrium distribution: it stays binomial with <i>p</i> = <i>v</i>/<i>V</i>. If the hole is smaller than a molecule diameter, the wall is impermeable and <i>n</i> = const: the distribution becomes deterministic (a δ-function).</p>' +
      '<h2 id="t9">9. Finite molecule size and impurity</h2>' +
      '<p>The ideal-gas model assumes point particles. For disks of radius <i>r</i> the centre cannot come closer than <i>r</i> to a wall, so the program computes <i>p</i> from the accessible area. Besides, disks cannot overlap (excluded volume), which creates correlations: at high density the fluctuations become <b>smaller</b> than binomial (problem 2.14, item 6). An impurity of large molecules occupies part of the volume and pushes the main molecules around; you can study the number of molecules of each component separately.</p>' +
      '<h2 id="t10">10. Problems from the book and how to check them in the demo</h2>' +
      '<table class="tasks"><tr><th>No.</th><th>Problem</th><th>Experiment in the program</th></tr>' +
      '<tr><td>1.10</td><td>Bernoulli for a gas: a variable equal to 1 if the tagged molecule is in the volume; the number of particles in the volume for <i>N</i> = 1.</td><td>Turn on the tagged molecule; set <i>N</i> = 1 and compare the histogram with the Bernoulli distribution.</td></tr>' +
      '<tr><td>1.11</td><td>Dialogue of particles in a vessel with a nook.</td><td>Watch the tagged molecule: how long it stays inside, how often it enters and leaves.</td></tr>' +
      '<tr><td>1.12</td><td>Two particles in a nook, <i>p</i> = 0.1: enumeration and the binomial distribution.</td><td>Experiment "Problem 1.12". Expected P(0) = 0.81, P(1) = 0.18, P(2) = 0.01.</td></tr>' +
      '<tr><td>2.13</td><td>Adventures of the Very One: probabilities of events for the tagged molecule.</td><td>The fraction of time the tagged molecule is inside → <i>v</i>/<i>V</i>.</td></tr>' +
      '<tr><td>2.14</td><td>Molecules in a nook: which of mean, variance, entropy stay unchanged when the volume is moved, <i>N</i> and <i>V</i> change, atoms form molecules, atoms grow.</td><td>Change <i>N</i>, the volume fraction, the radius, try the dense gas; compare the mean and variance.</td></tr>' +
      '<tr><td>2.15</td><td>By how much exactly does each characteristic change.</td><td>Double <i>N</i>: mean and variance double, σ/⟨<i>n</i>⟩ decreases by √2.</td></tr>' +
      '<tr><td>2.16</td><td>Binomial versus Poisson.</td><td>Show both curves and compare them for different <i>v</i>/<i>V</i>.</td></tr>' +
      '<tr><td>2.23</td><td>From binomial to Poisson: <i>N</i> → ∞, <i>p</i> → 0, <i>Np</i> = const.</td><td>Experiment "Poisson limit"; increase <i>N</i> while decreasing <i>v</i>/<i>V</i>.</td></tr>' +
      '<tr><td>3.3</td><td>A volume slightly smaller than the whole vessel: Poisson distribution for particles in the remaining part.</td><td>Experiment "Problem 3.3", curve "Poisson for <i>N</i> − <i>n</i>".</td></tr>' +
      '</table>')
}

  
zh = {
    # меню «Цвета» и легенда под сосудом
    'colorsMenu': '颜色',
    'zoomLabel': '比例',
    'zoomAll': '全范围 0…N',
    'colMolTitle': '分子',
    'colMolRegion': '区域内 / 区域外',
    'colMolSpeed': '按速度',
    'colMolOrigin': '按初始位置',
    'colHistTitle': '直方图',
    'colHistOne': '单色',
    'colHistSigma': '按偏离 ⟨n⟩ 的程度（σ、2σ）',
    'colSchemeTitle': '配色方案',
    'colScheme_color': '彩色',
    'colScheme_contrast': '高对比度（投影仪）',
    'colScheme_bw': '黑白（用于打印和引用）',
    'legIn': '在区域 v 内',
    'legOut': '在区域外',
    'legImp': '杂质',
    'legTag': '“最特别的那个”',
    'legSpeed': '慢 → 快',
    'legStartIn': '起始于区域内',
    'legStartOut': '起始于区域外',
    'tocExtra': '区域形状与分子',
    'preset112': '两个分子：概率 P(0)、P(1)、P(2)（习题 1.12）',
    'presetBinom': '二项分布：区域为容器的一半',
    'presetPoisson': '大容器中的小区域 → 泊松分布',
    'preset33': '区域几乎占满容器：N − n 的泊松分布（习题 3.3）',
    'presetHole': '通过小孔填充区域：向平衡弛豫',
    'presetDense': '稠密气体：涨落小于二项分布',
    'presetImp': '含大分子杂质的气体',
    'presetCorner': '容器角落中的阴影区域（如习题插图）',
    'presetBigV': '容器加倍、区域不变（改变 V）',
    'presetDiatomic': '原子结合成双原子分子',
    'presetBigAtoms': '大尺寸原子（排除体积）',
    'presetFew': '少量分子：分布的离散性',
    'secVessel': '容器与区域',
    'Wv': '容器宽度（体积 V）',
    'shape': '选定区域的形状',
    'shapeStrip': '靠左壁的条带',
    'shapeCorner': '角落中的矩形',
    'diatomic': '将原子结合成双原子分子',
    'hole': '小孔大小（占区域边长的比例）',
    'pairsNote': 'n 为原子数；理论：每个分子 2 个原子',
    'frac': '容器体积占比 v/V',
    'theoryExtra': '<h2 id="t11">11. 区域形状、容器体积与双原子分子</h2><p>分子数的分布只取决于面积比 <i>p</i> = <i>v</i>/<i>V</i>，与区域形状无关：程序中区域可以是靠壁的条带，也可以是容器角落中的矩形（如习题插图）。区域不变而容器增大时，<i>p</i> 和 ⟨<i>n</i>⟩ = <i>Np</i> 减小，相对涨落增大。</p><p>若原子两两结合成双原子分子，它们成对地进出区域。区域内分子数 <i>k</i> 服从参数为 <i>N</i>/2 和 <i>p</i> 的二项分布，原子数 <i>n</i> ≈ 2<i>k</i>，因此</p><div class="eq">⟨n⟩ = Np,&nbsp;&nbsp; σ² ≈ 4·' + F('N', '2') + '·p(1 − p) = 2Np(1 − p),</div><p>即均值不变，方差加倍（习题 2.14）。直方图中偶数 <i>n</i> 占优。</p>',
    'langName': '中文',
    'appTitle': '选定体积中的粒子',
    'kicker': '统计物理 · 交互式演示',
    'appSubtitle': '理想气体分子在容器中假想选定区域内数目的涨落：伯努利分布、二项分布、泊松分布与马尔可夫动力学。',
    'menuDemo': '演示',
    'menuTheory': '理论部分',
    'menuAuthors': '作者',
    'menuLanguage': '语言',
    'back': '← 菜单',
    'play': '▶ 开始',
    'pause': '⏸ 暂停',
    'reset': '⟲ 重新开始',
    'clearStats': '清除统计',
    'secStats': '统计',
    'secPresets': '预设实验',
    'presetNone': '— 选择实验 —',
    'secParticles': '分子',
    'N': '分子数 N',
    'r': '分子半径 r',
    'u': '温度（热速度）',
    'secVolume': '选定体积',
    'secWall': '隔板',
    'wall': '在体积边界设置不可穿透的隔板',
    'secImp': '杂质',
    'impN': '杂质分子数',
    'impR': '杂质分子半径',
    'count': '在体积内计数',
    'countMain': '主要分子',
    'countImp': '杂质分子',
    'countAll': '全部分子',
    'secSim': '模拟',
    'speed': '模拟速度',
    'init': '初始状态',
    'initUniform': '均匀分布',
    'initOutside': '全部在体积外',
    'initInside': '全部在体积内',
    'tagged': '标记一个分子（“最特别的那个”）',
    'showBinom': '二项分布',
    'showPois': '泊松',
    'showGauss': '高斯',
    'vesselTitle': '容器',
    'histTitle': '概率分布 P(n)',
    'timeTitle': '随时间的变化 n(t)',
    'legExp': '实验',
    'legBinom': '二项分布',
    'legPois': '泊松分布',
    'legPoisMirror': 'N − n 的泊松分布',
    'legGauss': '高斯分布',
    'legMean': '⟨n⟩ ± σ（理论）',
    'axisN': 'n',
    'axisP': 'P(n)',
    'axisT': 't，任意单位',
    'axisNt': 'n(t)',
    'noData': '点击“开始”以收集统计数据',
    'closedNote': '小孔小于分子直径——隔板不可穿透，体积内分子数守恒',
    'stN': '当前体积内分子数 n',
    'stSamples': '样本数',
    'stP': 'p = v/V（可达面积）',
    'stMean': '平均值 ⟨n⟩',
    'stVar': '方差 σ²',
    'stRel': '相对涨落 σ/⟨n⟩',
    'stTag': '被标记分子处于体积内的时间比例',
    'colExp': '实验',
    'colTheory': '理论',
    # страница авторов
    'authUniv': '莫斯科国立罗蒙诺索夫大学',
    'authFaculty': '计算数学与控制论系',
    'author1': '基尔斯伯格·阿琳娜·帕夫洛夫娜',
    'author2': '切里亚皮娜·安娜·谢尔盖耶夫娜',
    'authSupervisor': '指导教师：奥尔加·亚历山德罗夫娜·奇奇吉娜',
    'authLecturer': '讲师：基里尔·谢尔盖耶维奇·格里戈里耶夫',
    'tocRefs': '参考文献',
    'theoryRefs': '<h2 id="t12">参考文献</h2><p>O. A. Chichigina.《物理量的概率分布：习题集》. 莫斯科：莫斯科国立大学物理系，2026. 习题 1.10–1.12、2.13–2.16、2.23、3.3。</p>',
    'theoryHtml': (
      '<nav class="toc"><a href="#t1">模型</a><a href="#t2">伯努利</a><a href="#t3">二项分布</a><a href="#t4">泊松</a><a href="#t5">高斯</a><a href="#t6">v ≈ V</a><a href="#t7">马尔可夫过程</a><a href="#t8">小孔</a><a href="#t9">尺寸与杂质</a><a href="#t10">习题</a></nav>' +
      '<h2 id="t1">1. 模型</h2>' +
      '<p>考虑理想气体的二维模型：<i>N</i> 个分子在面积为 <i>V</i>（长 <i>a</i>，宽 <i>b</i>）的容器中运动，彼此之间以及与器壁发生弹性碰撞。在容器中假想地选定一块面积为 <i>v</i> 的区域（屏幕上以阴影表示）。某一时刻位于该区域内的分子数 <i>n</i> 是一个取值为 0, 1, …, <i>N</i> 的<b>离散随机变量</b>。</p>' +
      '<p>屏幕上，选定区域内的分子为实心，区域外的分子为空心，与习题 2.14 的插图一致。</p>' +
      '<h2 id="t2">2. 单个分子：伯努利分布</h2>' +
      '<p>在平衡态下，分子出现在容器内任一点的可能性相同，因此在选定区域内找到它的概率等于面积之比：</p>' +
      '<div class="eq">p = ' + F('v', 'V') + ',&nbsp;&nbsp; q = 1 − p。</div>' +
      '<p>变量 <i>n</i><sub>1</sub> = 1（在内）或 0（在外）服从伯努利分布：⟨<i>n</i><sub>1</sub>⟩ = <i>p</i>，σ² = <i>p</i>(1 − <i>p</i>)。打开“标记一个分子”，它在体积内停留的时间比例趋于 <i>p</i>（习题 1.10 第 1 问、2.13）。</p>' +
      '<h2 id="t3">3. N 个分子：二项分布</h2>' +
      '<p>理想气体分子之间没有相互作用，因此不同分子进入区域的事件相互独立，<i>n</i> 是 <i>N</i> 个独立伯努利变量之和：</p>' +
      '<div class="eq">P<sub>N</sub>(n) = ' + F('N!', 'n!(N − n)!') + ' p<sup>n</sup>(1 − p)<sup>N−n</sup>，</div>' +
      '<div class="eq">⟨n⟩ = Np,&nbsp;&nbsp; σ² = Np(1 − p),&nbsp;&nbsp; ' + F('σ', '⟨n⟩') + ' = √' + F('1 − p', 'Np') + '。</div>' +
      '<p>相对涨落按 1/√<i>N</i> 减小——这就是气体宏观密度几乎不涨落的原因。该分布有两个参数（<i>N</i>，<i>p</i>）。</p>' +
      '<p><b>例（习题 1.12）。</b><i>N</i> = 2，<i>p</i> = 0.1。枚举：两个都在外 0.9·0.9 = 0.81；一个在内 2·0.1·0.9 = 0.18；两个都在内 0.01。总和为 1，满足归一化。</p>' +
      '<h2 id="t4">4. 泊松极限</h2>' +
      '<p>若 <i>N</i> → ∞，<i>p</i> → 0 且 <i>Np</i> = λ = 常数（大容器中的小体积，<i>v</i> ≪ <i>V</i>），将 <i>p</i> = λ/<i>N</i> 代入并利用第二个重要极限（习题 2.23），得</p>' +
      '<div class="eq">P(n) = ' + F('λ<sup>n</sup>', 'n!') + ' e<sup>−λ</sup>,&nbsp;&nbsp; ⟨n⟩ = σ² = λ = n<sub>0</sub>v，</div>' +
      '<p>其中 <i>n</i><sub>0</sub> = <i>N</i>/<i>V</i> 为浓度。该分布只有一个参数，只取决于浓度和选定体积的大小，而与容器大小无关（习题 2.16）。</p>' +
      '<h2 id="t5">5. 高斯极限</h2>' +
      '<p>当 <i>Np</i>(1 − <i>p</i>) ≫ 1 时，二项分布趋于正态分布（习题 3.12）：</p>' +
      '<div class="eq">P(n) ≈ ' + F('1', '√(2πσ²)') + ' exp[ −' + F('(n − Np)²', '2σ²') + ' ],&nbsp;&nbsp; σ² = Np(1 − p)。</div>' +
      '<h2 id="t6">6. 接近整个容器的体积（习题 3.3）</h2>' +
      '<p>条件 <i>n</i> ≫ 1 并不足以过渡到连续描述。若 <i>v</i> 略小于 <i>V</i>，则 <i>n</i> 只取少数几个值 <i>N</i>、<i>N</i> − 1、<i>N</i> − 2、…… 此时小量是区域<b>外</b>的分子数 <i>m</i> = <i>N</i> − <i>n</i>，它服从泊松分布：</p>' +
      '<div class="eq">P(n) = ' + F('λ<sup>N−n</sup> e<sup>−λ</sup>', '(N − n)!') + ',&nbsp;&nbsp; λ = N(1 − p)。</div>' +
      '<p>当 <i>p</i> > 0.5 时，程序绘制的正是这条“镜像”泊松曲线。</p>' +
      '<h2 id="t7">7. 随时间的演化：离散马尔可夫过程</h2>' +
      '<p>被标记的分子不断进入和离开区域（电报信号）。若每次停留期间它都经历多次碰撞而“忘记”过去，则区域内停留时间 <i>t</i><sub>1</sub> 和区域外停留时间 <i>t</i><sub>2</sub> 服从指数分布，单位时间的跃迁概率为常数：γ<sub>−</sub> = 1/⟨<i>t</i><sub>1</sub>⟩（离开），γ<sub>+</sub> = 1/⟨<i>t</i><sub>2</sub>⟩（进入）。于是</p>' +
      '<div class="eq">p = ' + F('⟨t<sub>1</sub>⟩', '⟨t<sub>1</sub>⟩ + ⟨t<sub>2</sub>⟩') + ' = ' + F('γ<sub>+</sub>', 'γ<sub>+</sub> + γ<sub>−</sub>') + '。</div>' +
      '<p>分子数 <i>n</i> 构成生灭过程：<i>n</i> → <i>n</i> + 1 的速率为 (<i>N</i> − <i>n</i>)γ<sub>+</sub>，<i>n</i> → <i>n</i> − 1 的速率为 <i>n</i>γ<sub>−</sub>。主方程为</p>' +
      '<div class="eq">' + F('dP<sub>n</sub>', 'dt') + ' = (N − n + 1)γ<sub>+</sub>P<sub>n−1</sub> + (n + 1)γ<sub>−</sub>P<sub>n+1</sub> − [(N − n)γ<sub>+</sub> + nγ<sub>−</sub>]P<sub>n</sub>。</div>' +
      '<p>其稳态解就是二项分布。平均值按指数规律弛豫：</p>' +
      '<div class="eq">⟨n⟩(t) = Np + (n(0) − Np) e<sup>−t/τ</sup>,&nbsp;&nbsp; 1/τ = γ<sub>+</sub> + γ<sub>−</sub>。</div>' +
      '<p>选择初始状态“全部在体积外”，即可在 <i>n</i>(<i>t</i>) 图上观察弛豫过程。</p>' +
      '<h2 id="t8">8. 带小孔的隔板</h2>' +
      '<p>设区域由一面带有长度为 <i>c</i> 的小孔的隔板隔开。在二维气体中，通过小孔的分子流为</p>' +
      '<div class="eq">J = ' + F('n<sub>s</sub> ⟨|v|⟩ c', 'π') + '，</div>' +
      '<p>其中 <i>n</i><sub>s</sub> 为浓度，⟨|<i>v</i>|⟩ ∝ √<i>T</i> 为平均速率。因此，减小小孔或降低温度会<b>减慢</b>分子交换（τ 和 <i>n</i>(<i>t</i>) 的关联时间增大），但<b>不会改变</b>平衡分布：它仍是 <i>p</i> = <i>v</i>/<i>V</i> 的二项分布。若小孔小于分子直径，隔板不可穿透，<i>n</i> = 常数，分布变为确定性的（δ 函数）。</p>' +
      '<h2 id="t9">9. 分子的有限尺寸与杂质</h2>' +
      '<p>理想气体模型假设粒子为质点。对于半径为 <i>r</i> 的圆盘，其中心不能靠近器壁小于 <i>r</i> 的距离，因此程序按可达面积计算 <i>p</i>。此外，圆盘不能重叠（排除体积），由此产生关联：在高密度下涨落<b>小于</b>二项分布的涨落（习题 2.14 第 6 问）。大分子杂质占据部分体积并与主要分子碰撞；可以分别研究每种组分的分子数分布。</p>' +
      '<h2 id="t10">10. 习题集中的题目及其在演示中的验证</h2>' +
      '<table class="tasks"><tr><th>题号</th><th>题目</th><th>程序中的实验</th></tr>' +
      '<tr><td>1.10</td><td>气体的伯努利分布：被标记分子在体积内时取 1 的变量；<i>N</i> = 1 时体积内的粒子数。</td><td>打开被标记的分子；设 <i>N</i> = 1，将直方图与伯努利分布比较。</td></tr>' +
      '<tr><td>1.11</td><td>带角落的容器中粒子的对话。</td><td>观察被标记的分子：它在内部停留多久，多久进出一次。</td></tr>' +
      '<tr><td>1.12</td><td>角落里的两个粒子，<i>p</i> = 0.1：枚举与二项分布。</td><td>实验“习题 1.12”。预期 P(0) = 0.81，P(1) = 0.18，P(2) = 0.01。</td></tr>' +
      '<tr><td>2.13</td><td>“最特别的那个”的奇遇：被标记分子各事件的概率。</td><td>被标记分子在体积内的时间比例 → <i>v</i>/<i>V</i>。</td></tr>' +
      '<tr><td>2.14</td><td>角落里的分子：移动体积、改变 <i>N</i> 和 <i>V</i>、原子结合成分子、原子变大时，均值、方差、熵中哪些不变。</td><td>改变 <i>N</i>、体积比例、半径，尝试稠密气体；比较均值与方差。</td></tr>' +
      '<tr><td>2.15</td><td>各特征量具体变化多少（几倍）。</td><td>使 <i>N</i> 加倍：均值和方差加倍，σ/⟨<i>n</i>⟩ 减小为原来的 1/√2。</td></tr>' +
      '<tr><td>2.16</td><td>二项分布与泊松分布的比较。</td><td>同时显示两条曲线，在不同 <i>v</i>/<i>V</i> 下比较。</td></tr>' +
      '<tr><td>2.23</td><td>从二项分布到泊松分布：<i>N</i> → ∞，<i>p</i> → 0，<i>Np</i> = 常数。</td><td>实验“泊松极限”；增大 <i>N</i> 的同时减小 <i>v</i>/<i>V</i>。</td></tr>' +
      '<tr><td>3.3</td><td>略小于整个容器的体积：剩余部分中粒子数的泊松分布。</td><td>实验“习题 3.3”，曲线“N − n 的泊松分布”。</td></tr>' +
      '</table>')
}

  
I18N = {'ru': ru, 'en': en, 'zh': zh}
LANGS = ['ru', 'en', 'zh']
