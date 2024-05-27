import matplotlib.pyplot as plt
import numpy as np

# Les données fournies
data = [
    (1595623618, 3088768252, 0.00018887066609072224), (250522415, 3088768677, 0.00018887066609070744),
    (250522418, 250522505, 0.000188870666090704), (142123588, 250522418, 0.00018887066609033258),
    (1380535876, 1595623618, 0.00018887066461234416), (250651659, 3247392176, 0.00018882561264507198),
    (1380535868, 1380535876, 0.00018672854897399164), (1380535292, 5288370320, 0.00018652437748489545),
    (252624668, 1380535292, 0.00018652437748489534), (250651711, 252624668, 0.00018652437748447638),
    (1380535868, 5288370320, 0.00018652437748327335), (252624528, 252624541, 0.00018652433941730755),
    (250651711, 252624540, 0.0001865243393582884), (250651654, 250651659, 0.00018648783752714024),
    (252624528, 252624540, 0.00018592872067158802), (250651654, 3245831223, 0.00018533124981219898),
    (252624541, 3245831223, 0.00018533124981219548), (250522415, 8880257522, 0.00012321649711054443),
    (250522505, 8880257522, 0.00012321649711053508), (30342519, 3088768677, 0.00012303199262292234),
    (30342519, 250521515, 0.00012303199262288223), (250521515, 3088768252, 0.00012303199261183892),
    (30342490, 3088768252, 6.58412354569427e-05), (30342490, 1631630771, 6.584123544578846e-05),
    (1631630771, 3088768677, 6.584123544573856e-05), (250522415, 250522505, 6.566373578297761e-05),
    (130125942, 2949294278, 2.372110267074205e-06), (130125942, 3051804027, 2.372110267074205e-06),
    (252624868, 3051804027, 2.3721102670742037e-06), (1380535821, 2949294278, 2.3721095749269674e-06),
    (385216709, 472441181, 2.363347666923685e-06), (250651665, 385216709, 2.3633078075129855e-06),
    (250651664, 250651665, 2.363307807512983e-06), (250651659, 250651662, 2.3633048657470797e-06),
    (250651662, 250651664, 2.363304865747077e-06), (252624860, 252624868, 2.2452908676714e-06),
    (1380535821, 1380535827, 2.1636820578827165e-06), (1380535827, 1380535876, 2.163682048477843e-06),
    (252624462, 472441181, 1.9977496189189055e-06), (252624462, 385210396, 1.5142785418687242e-06),
    (385210326, 385210396, 1.5064839438868136e-06), (385210326, 2826973422, 1.4982100875566893e-06),
    (252624858, 252624860, 1.4014997802649922e-06), (252624837, 252624858, 1.387054420925135e-06),
    (252624837, 2826973422, 1.3801721531446165e-06), (252624541, 1380535326, 1.201447761998595e-06),
    (250651654, 1380535326, 1.1830305669142675e-06), (252624860, 385213230, 8.438557485842434e-07),
    (252624522, 252624528, 6.049169433487979e-07), (252624522, 252624540, 6.049168759266315e-07),
    (385213230, 385213238, 6.042066978389689e-07), (385209974, 385213238, 6.042066737064482e-07),
    (252624463, 385209974, 6.042066088515325e-07), (252624462, 252624463, 4.835463391495773e-07),
    (252624463, 472441181, 3.656023509096073e-07), (252624463, 252624470, 2.4392699751710223e-07),
    (252624470, 385214815, 2.4392697177019087e-07), (385213230, 385214815, 2.4021184401181836e-07),
    (1380535868, 4167727334, 2.0893303396944498e-07), (1380535821, 4167727334, 2.0893303200121075e-07),
    (138063232, 250651667, 1.2702666979826225e-07), (138063232, 252624868, 1.2702666976374084e-07),
    (250651667, 2826973422, 1.1822435049666985e-07), (250651660, 3247392176, 3.785405823461969e-08),
    (250651652, 250651653, 3.780830119461359e-08), (250651653, 250651660, 3.780830109648083e-08),
    (250651652, 250651654, 1.9183926313592632e-08), (250651628, 250651652, 1.8624375207781482e-08),
    (250651628, 1380535326, 1.8624375163305642e-08), (252624858, 385210398, 1.4632647396139218e-08),
    (385210397, 385210398, 1.0899462786241851e-08), (385210397, 385210670, 9.491094316181606e-09),
    (252609234, 3247392176, 8.942126184717006e-09), (252624407, 2905906551, 8.94210318636684e-09),
    (252609235, 2905906551, 8.942103186366826e-09), (252609234, 252609235, 8.942103186366819e-09),
    (252609239, 252624407, 8.938949207162205e-09), (252609239, 1944554014, 8.938891718037376e-09),
    (252624415, 1944554014, 8.8968776566525e-09), (250651667, 252624431, 8.868494108600454e-09),
    (252624415, 252624431, 8.868435051264974e-09), (385210326, 385210397, 8.41422669210833e-09),
    (385210396, 385210670, 7.849649620363339e-09), (252624837, 385210397, 7.005153372156538e-09),
    (385210398, 385214815, 3.733685179762075e-09), (252624463, 385210670, 1.660385215617103e-09),
    (1256603554, 11198106783, 4.766766180035885e-11), (250651660, 1256603554, 4.7667661800358456e-11),
    (344579429, 11198106783, 4.766766180035843e-11), (252608994, 1380535748, 4.723761551541133e-11),
    (252608994, 344579429, 4.723674809826892e-11), (1380535748, 1380535805, 4.689878541861091e-11),
    (250651711, 250651712, 4.38350424010924e-11), (250651699, 250651704, 4.3834787644108686e-11),
    (250651704, 250651705, 4.383478764410694e-11), (250651714, 1767023704, 4.383470412074953e-11),
    (250651705, 1767023704, 4.3834704120747205e-11), (250651712, 250651714, 4.383470412073962e-11),
    (385217368, 385217371, 4.305286548665849e-11), (385216709, 385217368, 4.305286548665723e-11),
    (385217371, 1944554014, 4.3052865486651314e-11), (252623725, 1380535805, 3.813030252348804e-11),
    (250651685, 252623725, 3.5235271795391224e-11), (250651685, 1380535836, 3.506636290543733e-11),
    (250651699, 2876265975, 3.490386945222066e-11), (1380535836, 2876265975, 3.475306690271089e-11),
    (252624415, 252624462, 2.9391421118529076e-11), (252623697, 252623699, 9.090424913003341e-12),
    (250651699, 252623697, 8.937604695507444e-12), (252623594, 1380535805, 8.770205659364357e-12),
    (252623594, 252623699, 8.755207931752608e-12), (250651664, 3126239261, 3.32796101217937e-12),
    (252624407, 3126239261, 3.327961011935263e-12), (1380535917, 8038146837, 2.93907045220413e-12),
    (252623725, 8038146837, 2.9390704498654165e-12), (250651828, 251629672, 2.515809877014547e-12),
    (362557592, 10750486717, 2.509232116991925e-12), (251629681, 3493090054, 2.5090715661618167e-12),
    (250651838, 362557592, 2.5087718268932794e-12), (250651838, 338905427, 2.5087631276110644e-12),
    (251627997, 2314448959, 2.504900699551814e-12), (2314448955, 10750486723, 2.504663086564222e-12),
    (250651833, 2516374130, 2.498518761277504e-12), (250651833, 251629681, 2.49840978084178e-12),
    (251629672, 2516374130, 2.495136253565934e-12), (2314448955, 2314448959, 2.478816298104087e-12),
    (60129598, 251627911, 2.2240891340343454e-12), (251627911, 251627945, 2.220897192979348e-12),
    (251627945, 251627997, 2.212843294869678e-12), (60129595, 354586115, 2.1952782651266128e-12),
    (60129595, 60129598, 2.1946822581949363e-12), (146114824, 354586115, 2.1843500574269168e-12),
    (146114819, 4547549638, 2.07308272382524e-12), (146114819, 146114824, 2.073082713099352e-12),
    (146111102, 4547549636, 2.07144609159827e-12), (146103671, 146111102, 2.0399068515280325e-12),
    (250651807, 252624351, 2.02050671679178e-12), (1380535917, 2828531958, 2.0135141105010925e-12),
    (1380536194, 2828531958, 2.013418073888396e-12), (252624351, 1380536194, 2.012488423343801e-12),
    (250651807, 1510811733, 1.9873599332340516e-12), (322716476, 1510811733, 1.98735992999175e-12),
    (250651828, 322716475, 1.9867632390966453e-12), (322716475, 322716476, 1.986763238489017e-12),
    (146103664, 146103671, 1.9855292989225014e-12), (1380535876, 1595623621, 1.9508391428966468e-12),
    (1595623618, 1595623621, 1.950809136325968e-12), (2309566304, 2453063134, 1.8835046877395282e-12),
    (142156039, 2309566300, 1.882884947620107e-12), (2309566300, 2309566304, 1.8823793277237304e-12),
    (1027210735, 2223055986, 1.8532323335052345e-12), (146111192, 2223055986, 1.8532323289911823e-12),
    (146103664, 146111192, 1.8519962544281717e-12), (338905427, 3493090054, 1.8458325799789353e-12),
    (1027210735, 2453063134, 1.8084088824736248e-12), (255683619, 5546032639, 1.7180137981031049e-12),
    (142123761, 1624229275, 1.6920140158613707e-12), (142142186, 255683619, 1.6724334579974883e-12),
    (1624229275, 5111371760, 1.6671085430870975e-12), (142142186, 5111371760, 1.6671085414416634e-12),
    (250651842, 10750486717, 1.6046160095548592e-12), (250651842, 10750486723, 1.603512298548345e-12),
    (142123599, 5546032639, 1.3938886208707413e-12), (264480583, 264480915, 1.3777549834835356e-12),
    (378275540, 474997692, 1.3743997814891547e-12), (250651747, 2445659130, 1.374399764887802e-12),
    (474997692, 2445659130, 1.3743997484117891e-12), (251629985, 378275540, 1.3740462586589396e-12),
    (142123588, 8880257540, 1.371969823802156e-12), (251629985, 5288260347, 1.3386069413491524e-12),
    (1380535868, 5288260347, 1.3385940896154104e-12), (142123598, 142144557, 1.3180736338256473e-12),
    (142144557, 2822030163, 1.3151865435184827e-12), (250651747, 378283439, 1.2928328662345897e-12),
    (142123598, 5546032638, 1.1728226186228132e-12), (142123798, 142156039, 1.147335843293966e-12),
    (142155956, 1624229293, 1.0944329708646098e-12), (142123761, 1624229293, 1.094399740869215e-12),
    (142123756, 142155956, 1.0612056675702682e-12), (142123756, 142123798, 1.0609359867856995e-12),
    (30342516, 264480915, 1.0411496703814087e-12), (4547549635, 4547549638, 1.0385283893022881e-12),
    (4547549635, 4547549636, 1.0368936555144906e-12), (4547549636, 4547549637, 1.0345561994782007e-12),
    (4547549637, 4547549638, 1.0345561736282823e-12), (250651798, 250651844, 9.38589663901354e-13),
    (250651798, 1380535917, 9.26192320208751e-13), (10750486716, 10750486717, 9.063009452286743e-13),
    (10750486716, 10750486723, 9.027522107806411e-13), (250651778, 250651844, 8.746905794898937e-13),
    (142123599, 5546032638, 8.487607037841111e-13), (30342516, 2822030163, 8.292961525211628e-13),
    (1380535821, 2949294279, 8.026605747164532e-13), (2949294278, 2949294279, 8.026481739047839e-13),
    (3244457467, 3244457512, 7.933526842205552e-13), (250651778, 3244457467, 7.93352652916861e-13),
    (378283439, 3244457512, 7.933526482702694e-13), (142156008, 2352446902, 7.359202368221579e-13),
    (142156031, 142156039, 7.359202029380921e-13), (142156031, 2352446902, 7.359202014169683e-13),
    (142139110, 142156008, 7.356441336107839e-13), (142139056, 142139110, 7.356440645011896e-13),
    (142123588, 2822030114, 7.355017719378171e-13), (250522321, 250522731, 7.352800758205002e-13),
    (142139056, 142139060, 7.352800627431141e-13), (142139060, 142139064, 7.352800401991753e-13),
    (142139064, 142139067, 7.351664308624342e-13), (142139067, 3349843975, 7.350181733733025e-13),
    (250522321, 3349843975, 7.348392445970258e-13), (250522731, 2822030114, 7.264795028707568e-13),
    (264480583, 8880257540, 7.252074633723018e-13), (496015600, 1456850660, 7.240473930684956e-13),
    (142123761, 1456850660, 7.188776474603001e-13), (496015600, 496015614, 6.683350983008116e-13),
    (3493090054, 3493090057, 6.675146684523548e-13), (338905427, 3493090057, 6.671785273456332e-13),
    (142124054, 142124091, 6.656970279993528e-13), (264480583, 5109497998, 6.525562973648482e-13),
    (5109497998, 8880257540, 6.467763309952933e-13), (142124091, 496015614, 6.320848264056846e-13),
    (142144557, 264480880, 5.485295844092723e-13), (142144557, 142144561, 5.45641343135549e-13),
    (142123599, 142144561, 5.452669462147232e-13), (250651821, 250651828, 5.303478761038861e-13),
    (250651814, 250651821, 5.29633964114318e-13), (250651723, 250651792, 5.003423975459531e-13),
    (31114098, 378283439, 5.000257085658377e-13), (31114098, 250651723, 4.986707766047346e-13),
    (142123588, 264480549, 4.917608500672458e-13), (264480549, 2822030163, 4.859586544950212e-13),
    (142124040, 142124054, 4.437711206954163e-13), (344579428, 344579429, 4.421982626552622e-13),
    (252623780, 344579426, 4.40008645837115e-13), (252623772, 252623823, 4.3946864002294097e-13),
    (252623772, 252623780, 4.393691061434305e-13), (252624016, 2314448825, 4.3235481954997445e-13),
    (252624016, 362568141, 4.3208334161480604e-13), (252623823, 252624011, 4.320831173418534e-13),
    (252624011, 362568141, 4.3208299433833617e-13), (250651814, 2314448825, 4.265151983357922e-13),
    (354587736, 1866311071, 3.8369102804039795e-13), (146135445, 354588236, 3.8293122333154976e-13),
    (354587736, 354588236, 3.829091141216334e-13), (250651629, 252623699, 3.5154596428751135e-13),
    (250651629, 1380535748, 3.5147170737065504e-13), (30342734, 142156127, 3.433687090359283e-13),
    (142156127, 2223055992, 3.4269653250514446e-13), (344579427, 344579428, 3.3752691569487486e-13),
    (264480880, 264480915, 3.3660553494873964e-13), (344579424, 344579426, 3.365102725077523e-13),
    (344579424, 344579427, 3.3645294384742377e-13), (60129372, 60129374, 3.2692438171171197e-13),
    (60129374, 4462437292, 3.2563977451936857e-13), (5546032638, 5546032639, 3.24180096935801e-13),
    (60129372, 1866311071, 3.224796737172899e-13), (250651792, 1380535836, 3.204064813272575e-13),
    (251627910, 251627997, 2.927931722735343e-13), (146103661, 2223055994, 2.8419818879457603e-13),
    (2223055991, 2223055992, 2.8354828680767983e-13), (2223055991, 2223055994, 2.8354826837267574e-13),
    (146092784, 146097244, 2.401901400660314e-13), (30342734, 142124040, 2.3108872323155833e-13),
    (146097244, 146135445, 2.310483191148309e-13), (142123798, 142124054, 2.2314233485768294e-13),
    (142124026, 142124040, 2.1794972282470042e-13), (30342516, 264480880, 2.1200282509018088e-13),
    (142124017, 142124026, 2.0168471239555201e-13), (250651685, 250651782, 1.9317528217643854e-13),
    (251627910, 4462437292, 1.8537264394253702e-13), (250651782, 378268597, 1.8049073917606706e-13),
    (250651792, 378268597, 1.8049062706594104e-13), (354593046, 5110623272, 1.6606087985277868e-13),
    (494911158, 5110623272, 1.6370736354423755e-13), (146092784, 494911158, 1.6015216088896472e-13),
    (252623697, 2876265975, 1.5848635882909905e-13), (146103669, 146103680, 1.5322541876957408e-13),
    (146103661, 146103684, 1.5244601518628398e-13), (124269978, 2936621964, 1.510787518062691e-13),
    (142123598, 255684755, 1.510787344083727e-13), (255684755, 2936621964, 1.5107873438567795e-13),
    (146103680, 146103684, 1.5096243125052278e-13), (146092784, 1941409385, 1.5093605886436954e-13),
    (146092722, 1941409385, 1.5022847220131011e-13), (146135445, 3741947132, 1.4911526150792821e-13),
    (142123769, 142142207, 1.4815390062612949e-13), (142123769, 1624229268, 1.478347799287185e-13),
    (142142207, 142142213, 1.4237089473335252e-13), (30342734, 142123798, 1.3793956453120615e-13),
    (146103661, 146103664, 1.3358257091521163e-13), (60285361, 251627824, 1.311312893172468e-13),
    (251627824, 4462437292, 1.310014786892879e-13), (142123964, 142124017, 1.278685363330933e-13),
    (124269978, 142123595, 1.2182946448715687e-13), (142123761, 1624229268, 1.2154792376267524e-13),
    (344579423, 344579430, 1.209246507378879e-13), (344579283, 344579423, 1.20861966596764e-13),
    (142123964, 142123966, 1.18375794483989e-13), (146114873, 354586749, 1.1644387979473056e-13),
    (146114824, 354586749, 1.1620781307131974e-13), (60285361, 251627910, 1.0628546384674114e-13)
]

# Extraire les conductivités
conductivities = [item[2] for item in data]

plt.figure(figsize=(12, 6))
for idx, conductivity in enumerate(conductivities):
    color = 'r' if conductivity > 1e-5 else 'b'
    plt.plot([idx, idx], [1e-14, conductivity], color + '-', alpha=0.6)  # Tracer une ligne verticale

plt.yscale('log')
plt.xlabel('Index')
plt.ylabel('Conductivity')
plt.title('300 Biggest Conductivities of Edges ')
plt.grid(True, which="both", ls="--")
plt.show()
