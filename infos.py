import openai

# generate_BrainX.py
# ============================================
QS_TYPE = [
    "TF",
    "CHOICE",
    "TEXT"
]

KOCK_CHAPTERS = [
    (30, 49), (50, 73), (74, 109), (110, 141), (142, 166), (167, 196),
    (197, 217), (218, 236), (237, 256), (257, 272), (273, 304), (305, 332),
    (333, 354), (355, 374), (375, 398), (399, 405), (406, 426), (427, 453),
    (454, 476), (477, 493), (494, 505), (506, 527)
]

ORG_SYN2008_CHAPTERS = [
    (16, 38), (38, 77), (77, 104), (104, 124), (124, 160), (160, 186), (186, 218),
    (218, 263), (263, 282), (282, 299), (299, 327), (327, 378), (378, 416), (416, 450),
    (450, 468), (468, 510),(510, 544),(544, 562), (562, 610), (610, 630), (630, 670), 
    (670, 691), (691, 716), (723, 734), (738, 758), (766, 781)
]

# start from 49, end at 1581, step 8
PRINCIPLE_NEURAL_SCIENCE_CHAPTERS = [
    (49, 57), (57, 65), (65, 73), (73, 81), (81, 89), (89, 97), (97, 105), (105, 113),
    (113, 121), (121, 129), (129, 137), (137, 145), (145, 153), (153, 161), (161, 169),
    (169, 177), (177, 185), (185, 193), (193, 201), (201, 209), (209, 217), (217, 225),
    (225, 233), (233, 241), (241, 249), (249, 257), (257, 265), (265, 273), (273, 281),
    (281, 289), (289, 297), (297, 305), (305, 313), (313, 321), (321, 329), (329, 337),
    (337, 345), (345, 353), (353, 361), (361, 369), (369, 377), (377, 385), (385, 393),
    (393, 401), (401, 409), (409, 417), (417, 425), (425, 433), (433, 441), (441, 449),
    (449, 457), (457, 465), (465, 473), (473, 481), (481, 489), (489, 497), (497, 505),
    (505, 513), (513, 521), (521, 529), (529, 537), (537, 545), (545, 553), (553, 561),
    (561, 569), (569, 577), (577, 585), (585, 593), (593, 601), (601, 609), (609, 617),
    (617, 625), (625, 633), (633, 641), (641, 649), (649, 657), (657, 665), (665, 673),
    (673, 681), (681, 689), (689, 697), (697, 705), (705, 713), (713, 721), (721, 729),
    (729, 737), (737, 745), (745, 753), (753, 761), (761, 769), (769, 777), (777, 785),
    (785, 793), (793, 801), (801, 809), (809, 817), (817, 825), (825, 833), (833, 841),
    (841, 849), (849, 857), (857, 865), (865, 873), (873, 881), (881, 889), (889, 897),
    (897, 905), (905, 913), (913, 921), (921, 929), (929, 937), (937, 945), (945, 953),
    (953, 961), (961, 969), (969, 977), (977, 985), (985, 993), (993, 1001), (1001, 1009),
    (1009, 1017), (1017, 1025), (1025, 1033), (1033, 1041), (1041, 1049), (1049, 1057),
    (1057, 1065), (1065, 1073), (1073, 1081), (1081, 1089), (1089, 1097), (1097, 1105),
    (1105, 1113), (1113, 1121), (1121, 1129), (1129, 1137), (1137, 1145), (1145, 1153),
    (1153, 1161), (1161, 1169), (1169, 1177), (1177, 1185), (1185, 1193), (1193, 1201),
    (1201, 1209), (1209, 1217), (1217, 1225), (1225, 1233), (1233, 1241), (1241, 1249),
    (1249, 1257), (1257, 1265), (1265, 1273), (1273, 1281), (1281, 1289), (1289, 1297),
    (1297, 1305), (1305, 1313), (1313, 1321), (1321, 1329), (1329, 1337), (1337, 1345),
    (1345, 1353), (1353, 1361), (1361, 1369), (1369, 1377), (1377, 1385), (1385, 1393),
    (1393, 1401), (1401, 1409), (1409, 1417), (1417, 1425), (1425, 1433), (1433, 1441),
    (1441, 1449), (1449, 1457), (1457, 1465), (1465, 1473), (1473, 1481), (1481, 1489),
    (1489, 1497), (1497, 1505), (1505, 1513), (1513, 1521), (1521, 1529), (1529, 1537),
    (1537, 1545), (1545, 1553), (1553, 1561), (1561, 1569), (1569, 1577), (1577, 1581),
]

   

ORG_SYN2008_PATH_PDF = "data/neuroscience/books/pdfs/StructuralAndFunctionalOrganizationOfTheSynapsespringer2008/StructuralAndFunctionalOrganizationOfTheSynapsespringer2008.pdf"
ORG_SYN2008_PATH = "data/neuroscience/books/pdfs/StructuralAndFunctionalOrganizationOfTheSynapsespringer2008"

KOCH_PATH_PDF = "data/neuroscience/books/pdfs/Biophysics of Computation_ Information Processing in Single Neurons_Christof Koch/Biophysics of Computation_ Information Processing in Single Neurons_Christof Koch.pdf"
KOCH_PATH = "data/neuroscience/books/pdfs/Biophysics of Computation_ Information Processing in Single Neurons_Christof Koch"

PRINCIPLE_NEURAL_SCIENCE_PDF = "data/books/pdfs/Principle_of_NeuralScience/Principles of Neural Science (Sixth Edition) (Eric R. Kandel, John D. Koester etc.) (Z-Library).pdf"
PRINCIPLE_NEURAL_SCIENCE_PATH = "data/books/pdfs/Principle_of_NeuralScience"

BOOK_INFO_DICT = {
    "Koch":{
        "Full Name": "Biophysics of Computation_ Information Processing in Single Neurons_Christof Koch",
        "Chapters": KOCK_CHAPTERS,
        "PDF": KOCH_PATH_PDF,
        "source_path": KOCH_PATH,
    },

    "OrgSYN2008":{
        "Full Name": "StructuralAndFunctionalOrganizationOfTheSynapsespringer2008",
        "Chapters": ORG_SYN2008_CHAPTERS,
        "PDF": ORG_SYN2008_PATH_PDF,
        "source_path": ORG_SYN2008_PATH,
    },

    "PrincipleNeuralScience":{
        "Full Name": "Principles of Neural Science (Sixth Edition) (Eric R. Kandel, John D. Koester etc.) (Z-Library)",
        "Chapters": PRINCIPLE_NEURAL_SCIENCE_CHAPTERS,
        "PDF": PRINCIPLE_NEURAL_SCIENCE_PDF,
        "source_path": PRINCIPLE_NEURAL_SCIENCE_PATH,
    }
}
# ============================================


# collector.py
# ============================================
BASE_URL = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/"
PUB_BATCH_SIZE = 200  # 每次请求获取的最大文献数量，PubMed的限制
# ============================================


# utils_collect.py
# ============================================
JOURNALS = [
    "Nature communications",
    "The Journal of neuroscience : the official journal of the Society for Neuroscience",
    "Proceedings of the National Academy of Sciences of the United States of America",
    "Science advances",
    "Neuron",
    "Cell reports",
    "eLife",
    "Alzheimer's & dementia : the journal of the Alzheimer's Association",
    "Nature neuroscience",
    "The Journal of physiology"
]

LABEL_MATCHING_DIC = {
    "Nature communications": "NC",
    "The Journal of neuroscience : the official journal of the Society for Neuroscience": "JNeurosci",
    "Proceedings of the National Academy of Sciences of the United States of America": "PNAS",
    "Science advances": "Sci Adv",
    "Neuron": "Neuron",
    "Cell reports": "Cell Rep",
    "eLife": "eLife",
    "Alzheimer's & dementia : the journal of the Alzheimer's Association": "Alzheimer",
    "Nature neuroscience": "Nat. Neurosci",
    "The Journal of physiology": "J Physiol"
}

# Global Variables
# ============================================
BRAIN_X_BENCH_VERSION = 1.0

# ============================================


# API for LLM response
# ============================================

usage = "v3"
if usage == "v3":
    # Key TEXT
    openai.api_key = "sk-MSSwI7MgizQFSyUE64359c5000D64b518cCc7c00F30e0321"

    # Key CHOICE
    # openai.api_key = "sk-2MVtHUbwflfC57YH33D5478e03334d4cA2651e1fB7241f91"
    # openai.base_url = "https://api.v3.cm/v1/" #🇭🇰线路
    # openai.base_url = "https://us.vveai.com" #🇺🇸线路
    # openai.base_url = "https://run.v36.cm/v1/" #🇯🇵线路
    # openai.base_url = "https://api.aaai.vip/v1/" #国内线路
    openai.base_url = "https://api.vveai.com/v1/" #主站线路
    # openai.base_url = " https://api.gpt.ge/v1/"
    # openai.base_url = "https://guide1.lanjing.ai "
    openai.default_headers = {"x-foo": "true"}
    # ============================================
elif usage == "official":
    openai.api_key = "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"


elif usage == "free_use":
    openai.api_key = "sk-qze273cccad60a2609699a1f38ce5acbcc787cfcfc6fohDu"
    openai.base_url = "https://api.gptsapi.net/v1/"
    openai.default_headers = {"x-foo": "true"}