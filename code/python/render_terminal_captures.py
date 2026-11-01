import os
import re
from PIL import Image, ImageDraw, ImageFont

fontCandidates = [
    os.path.expanduser("~/.local/share/fonts/NerdFonts/JetBrainsMonoNerdFont-Regular.ttf"),
    "/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf",
    "/usr/share/fonts/truetype/liberation/LiberationMono-Regular.ttf"
]
fontPath = next((f for f in fontCandidates if os.path.exists(f)), None)

fontSize = 15
if fontPath:
    font = ImageFont.truetype(fontPath, fontSize)
    fontSmall = ImageFont.truetype(fontPath, 12)
else:
    font = ImageFont.load_default()
    fontSmall = ImageFont.load_default()

baseDir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
figuresDir = os.path.join(baseDir, "figures")
os.makedirs(figuresDir, exist_ok=True)

colorBg = (24, 24, 37)
colorTitleBar = (17, 17, 27)
colorBorder = (49, 50, 68)
colorDefault = (205, 214, 244)
colorDim = (108, 112, 134)
colorGreen = (166, 227, 161)
colorCyan = (137, 220, 235)
colorBlue = (137, 180, 250)
colorPeach = (250, 179, 135)
colorYellow = (249, 226, 175)
colorMauve = (203, 166, 247)
colorRed = (243, 139, 168)
colorWhite = (248, 248, 242)

def parseColoredLine(line):
    stripped = line.strip()
    if not stripped:
        return [("", colorDefault)]

    if line.startswith("tuong@workstation"):
        parts = []
        userHost = "tuong@workstation"
        rest = line[len(userHost):]
        parts.append((userHost, colorGreen))
        if ":" in rest:
            colonIdx = rest.index(":")
            parts.append((":", colorDim))
            rest2 = rest[colonIdx+1:]
            dollarIdx = rest2.index("$") if "$" in rest2 else -1
            if dollarIdx != -1:
                pathPart = rest2[:dollarIdx]
                cmdPart = rest2[dollarIdx:]
                parts.append((pathPart, colorCyan))
                parts.append((cmdPart[:1], colorRed))
                parts.append((cmdPart[1:], colorWhite))
            else:
                parts.append((rest2, colorWhite))
        else:
            parts.append((rest, colorWhite))
        return parts

    if line.startswith(">> "):
        return [(">> ", colorRed), (line[3:], colorWhite)]

    if set(stripped) == {"="}:
        return [(line, colorBlue)]

    if set(stripped) == {"-"} or set(stripped) == {"-", "+"}:
        return [(line, colorDim)]

    if any(h in stripped for h in ["STEP-BY-STEP", "SIMULATION SUMMARY", "BER DIVERSITY COMPARISON", "SHANNON CAPACITY"]):
        return [(line, colorPeach)]

    if any(stripped.startswith(prefix) for prefix in ["1. ZERO-FORCING", "2. MINIMUM MEAN", "3. SVD TRANSMIT", "[STBC", "[SDM", "PART 1:", "PART 2:", "PART 3:"]):
        return [(line, colorYellow)]

    if "STATUS: PASSED" in line or "STATUS: PERFECT RECOVERY" in line or "COMPLETE" in line:
        idx = line.find("STATUS:")
        if idx != -1:
            return [(line[:idx], colorDefault), (line[idx:], colorGreen)]
        return [(line, colorGreen)]

    if any(k in stripped for k in ["Channel Matrix H:", "Transmitted Symbols:", "Transmitted Symbol Vector", "Received Signals", "Received Vector", "Combiner Outputs", "Recovered Symbols", "Recovered Symbol Vector", "Precoded Vector", "Unitary Matrix", "Singular Value Matrix", "Weight Matrix", "Noise Variance"]):
        return [(line, colorCyan)]

    if "Error:" in line or "Norm Error:" in line:
        parts = []
        tokens = re.split(r'(Error:\s*[\d\.e+-]+|Norm Error:\s*[\d\.e+-]+)', line)
        for t in tokens:
            if "Error:" in t:
                parts.append((t, colorGreen))
            else:
                parts.append((t, colorDefault))
        return parts

    if "SNR(dB)" in line:
        return [(line, colorCyan)]

    if any(stripped.startswith(p) for p in ["0 dB", "5 dB", "10 dB", "15 dB", "20 dB", "25 dB", "-10 dB", "0.0", "4.0", "8.0", "12.0", "16.0", "20.0", "24.0", "-10.0", "-4.0", "2.0", "8.0", "14.0", "26.0", "30 dB"]):
        parts = []
        tokens = line.split("|")
        for i, tok in enumerate(tokens):
            if i == 0:
                parts.append((tok, colorYellow))
            elif i % 2 == 1:
                parts.append((tok, colorWhite))
            else:
                parts.append((tok, colorMauve))
            if i < len(tokens) - 1:
                parts.append(("|", colorDim))
        return parts

    if "< M A T L A B (R) >" in line or "Copyright 1984" in line or "R2025b" in line or "August 16" in line or "To get started" in line or "For product" in line:
        return [(line, colorDim)]

    return [(line, colorDefault)]

def renderTerminalImage(windowTitle, rawLines, outputPath):
    rawLines = ["ILLUSTRATION FROM EMBEDDED TEXT, NOT A LIVE EXECUTION CAPTURE"] + list(rawLines)
    charWidth = 9.0
    lineHeight = 24
    paddingX = 26
    paddingTop = 18
    paddingBottom = 24
    titleBarHeight = 38
    outerMargin = 16

    maxChars = max(len(l) for l in rawLines) if rawLines else 80
    contentWidth = int(max(maxChars * charWidth + 2 * paddingX, 980))
    contentHeight = len(rawLines) * lineHeight + paddingTop + paddingBottom

    imgWidth = contentWidth + 2 * outerMargin
    imgHeight = contentHeight + titleBarHeight + 2 * outerMargin

    img = Image.new("RGB", (imgWidth, imgHeight), (15, 15, 23))
    draw = ImageDraw.Draw(img)

    winX0 = outerMargin
    winY0 = outerMargin
    winX1 = imgWidth - outerMargin
    winY1 = imgHeight - outerMargin

    draw.rounded_rectangle([winX0, winY0, winX1, winY1], radius=10, fill=colorBg, outline=colorBorder, width=1)

    draw.rounded_rectangle([winX0, winY0, winX1, winY0 + titleBarHeight], radius=10, fill=colorTitleBar)
    draw.rectangle([winX0, winY0 + titleBarHeight - 10, winX1, winY0 + titleBarHeight], fill=colorTitleBar)
    draw.line([winX0, winY0 + titleBarHeight, winX1, winY0 + titleBarHeight], fill=colorBorder, width=1)

    btnY = winY0 + titleBarHeight // 2
    btnRadius = 6
    draw.ellipse([winX0 + 16, btnY - btnRadius, winX0 + 16 + 2*btnRadius, btnY + btnRadius], fill=(255, 95, 86))
    draw.ellipse([winX0 + 36, btnY - btnRadius, winX0 + 36 + 2*btnRadius, btnY + btnRadius], fill=(255, 189, 46))
    draw.ellipse([winX0 + 56, btnY - btnRadius, winX0 + 56 + 2*btnRadius, btnY + btnRadius], fill=(39, 201, 63))

    titleBox = draw.textbbox((0, 0), windowTitle, font=fontSmall)
    titleW = titleBox[2] - titleBox[0]
    titleX = (imgWidth - titleW) // 2
    titleY = winY0 + (titleBarHeight - (titleBox[3] - titleBox[1])) // 2
    draw.text((titleX, titleY), windowTitle, fill=colorDim, font=fontSmall)

    currY = winY0 + titleBarHeight + paddingTop
    for line in rawLines:
        colIdx = 0
        segments = parseColoredLine(line)
        for textPart, color in segments:
            if textPart:
                xPos = winX0 + paddingX + int(colIdx * charWidth)
                draw.text((xPos, currY), textPart, fill=color, font=font)
                colIdx += len(textPart)
        currY += lineHeight

    img.save(outputPath, "PNG", dpi=(300, 300))

stbcLines = [
    "tuong@workstation:~/DoAn_2026/code/matlab$ matlab -nodisplay -r \"mimo_stbc_2x2_recovery; exit;\"",
    "",
    "                            < M A T L A B (R) >",
    "                  Copyright 1984-2025 The MathWorks, Inc.",
    "             R2025b Update 7 (25.2.0.3360999) 64-bit (glnxa64)",
    "                              August 16, 2026",
    "",
    "To get started, type doc.",
    "For product information, visit www.mathworks.com.",
    "",
    ">> mimo_stbc_2x2_recovery",
    "========================================================",
    "     MIMO 2x2 ALAMOUTI STBC STEP-BY-STEP RECOVERY       ",
    "========================================================",
    "Channel Matrix H:",
    "    0.7000    0.3000",
    "    0.4000    0.6000",
    "",
    "Frobenius Norm Squared ||H||_F^2: 1.1000",
    "",
    "Transmitted Symbols:",
    "  s0 = +1.0000 +1.0000i",
    "  s1 = +1.0000 -1.0000i",
    "",
    "Received Signals (Noise = 0):",
    "  Time Slot 1, Antenna Rx1: r0 = +1.0000 +0.4000i",
    "  Time Slot 2, Antenna Rx1: r1 = -0.4000 -1.0000i",
    "  Time Slot 1, Antenna Rx2: r2 = +1.0000 -0.2000i",
    "  Time Slot 2, Antenna Rx2: r3 = +0.2000 -1.0000i",
    "",
    "Combiner Outputs (z = H_eff^H * r):",
    "  z0 = +1.1000 +1.1000i",
    "  z1 = +1.1000 -1.1000i",
    "",
    "Recovered Symbols (s_hat = z / ||H||_F^2):",
    "  s_hat0 = +1.0000 +1.0000i (Error: 2.22e-16)",
    "  s_hat1 = +1.0000 -1.0000i (Error: 2.22e-16)",
    "========================================================",
    ">> exit",
    "[Process completed - exit code 0]"
]

sdmLines = [
    "tuong@workstation:~/DoAn_2026/code/matlab$ matlab -nodisplay -r \"mimo_sdm_2x2_recovery; exit;\"",
    "",
    "                            < M A T L A B (R) >",
    "                  Copyright 1984-2025 The MathWorks, Inc.",
    "             R2025b Update 7 (25.2.0.3360999) 64-bit (glnxa64)",
    "                              August 16, 2026",
    "",
    "To get started, type doc.",
    "For product information, visit www.mathworks.com.",
    "",
    ">> mimo_sdm_2x2_recovery",
    "========================================================",
    "       MIMO 2x2 SDM STEP-BY-STEP SIGNAL RECOVERY        ",
    "========================================================",
    "Channel Matrix H:",
    "    0.7000    0.3000",
    "    0.4000    0.6000",
    "",
    "Transmitted Symbol Vector x:",
    "   1.0000 + 1.0000i",
    "   1.0000 - 1.0000i",
    "",
    "Received Vector y without precoding (y = H * x):",
    "   1.0000 + 0.4000i",
    "   1.0000 - 0.2000i",
    "",
    "--------------------------------------------------------",
    "1. ZERO-FORCING (ZF) DETECTION",
    "Weight Matrix W_ZF = pinv(H):",
    "    2.0000   -1.0000",
    "   -1.3333    2.3333",
    "",
    "Recovered Symbol Vector x_hat_ZF = W_ZF * y:",
    "   1.0000 + 1.0000i",
    "   1.0000 - 1.0000i",
    "",
    "ZF Norm Error: 1.01e-15",
    "--------------------------------------------------------",
    "2. MINIMUM MEAN SQUARE ERROR (MMSE) DETECTION",
    "Noise Variance: 0.0000",
    "Weight Matrix W_MMSE = inv(H'*H + sigma^2*I) * H':",
    "    2.0000   -1.0000",
    "   -1.3333    2.3333",
    "",
    "Recovered Symbol Vector x_hat_MMSE = W_MMSE * y:",
    "   1.0000 + 1.0000i",
    "   1.0000 - 1.0000i",
    "",
    "MMSE Norm Error: 3.85e-16",
    "--------------------------------------------------------",
    "3. SVD TRANSMIT PRECODING & RECEIVER DECOUPLING",
    "Unitary Matrix U (Left Singular Vectors):",
    "   -0.7298   -0.6837",
    "   -0.6837    0.7298",
    "",
    "Singular Value Matrix S:",
    "    1.0055         0",
    "         0    0.2984",
    "",
    "Unitary Matrix V (Right Singular Vectors / Precoding):",
    "   -0.7800   -0.6257",
    "   -0.6257    0.7800",
    "",
    "Precoded Vector x_tx = V * x:",
    "  -1.4058 - 0.1543i",
    "   0.1543 - 1.4058i",
    "",
    "Channel Output y_svd = H * x_tx:",
    "  -0.9377 - 0.5298i",
    "  -0.4697 - 0.9052i",
    "",
    "Decoupled Received Vector y_tilde = U' * y_svd = S * x:",
    "   1.0055 + 1.0055i",
    "   0.2984 - 0.2984i",
    "",
    "Recovered Vector x_hat_SVD = inv(S) * y_tilde:",
    "   1.0000 + 1.0000i",
    "   1.0000 - 1.0000i",
    "",
    "SVD Norm Error: 1.02e-15",
    "========================================================",
    ">> exit",
    "[Process completed - exit code 0]"
]

summaryLines = [
    "tuong@workstation:~/DoAn_2026$ python3 code/python/verify_all_simulations.py",
    "========================================================================================================",
    "                    MIMO 2x2 WIRELESS COMMUNICATIONS SIMULATION SUMMARY                   ",
    "========================================================================================================",
    "PART 1: STEP-BY-STEP SIGNAL RECOVERY VERIFICATION (Fixed H = [0.7 0.3; 0.4 0.6])",
    "--------------------------------------------------------------------------------------------------------",
    "[STBC Alamouti 2x2]",
    "  Transmitted: s0 = +1.0000 +1.0000i, s1 = +1.0000 -1.0000i",
    "  Received:    r0 = +1.0000 +0.4000i, r1 = -0.4000 -1.0000i (Rx1)",
    "               r2 = +1.0000 -0.2000i, r3 = +0.2000 -1.0000i (Rx2)",
    "  Combiner:    z0 = +1.1000 +1.1000i, z1 = +1.1000 -1.1000i (Frobenius norm sq = 1.1000)",
    "  Recovered:   s_hat0 = +1.0000 +1.0000i, s_hat1 = +1.0000 -1.0000i",
    "  Errors:      |s_hat0 - s0| = 1.11e-16, |s_hat1 - s1| = 1.11e-16 -> STATUS: PERFECT RECOVERY",
    "",
    "[SDM Multiplexing 2x2]",
    "  Zero-Forcing (ZF) Detection Error:         ||x_hat_ZF   - x|| = 1.05e-15 -> STATUS: PASSED",
    "  MMSE Detection (sigma=0) Error:            ||x_hat_MMSE - x|| = 1.29e-15 -> STATUS: PASSED",
    "  SVD Precoding & Decoupling Error:          ||x_hat_SVD  - x|| = 9.42e-16 -> STATUS: PASSED",
    "--------------------------------------------------------------------------------------------------------",
    "PART 2: BIT ERROR RATE (BER) DIVERSITY COMPARISON AT KEY EVALUATION SNRs",
    "--------------------------------------------------------------------------------------------------------",
    " SNR(dB) | SISO Theo   | SISO Sim    | SIMO SC     | SIMO MRC    | MISO 2x1    | MIMO 2x2 (Th / Sim) ",
    "---------+-------------+-------------+-------------+-------------+-------------+-----------------------",
    "    0 dB | 1.4645e-01  | 1.4536e-01  | 8.1468e-02  | 5.7912e-02  | 1.1510e-01  | 4.0258e-02 / 3.9880e-02",
    "    5 dB | 6.4183e-02  | 6.4004e-02  | 1.9926e-02  | 1.2046e-02  | 3.2858e-02  | 3.7190e-03 / 3.7860e-03",
    "   10 dB | 2.3269e-02  | 2.3110e-02  | 2.9920e-03  | 1.6020e-03  | 5.5282e-03  | 1.1336e-04 / 1.0600e-04",
    "   15 dB | 7.7230e-03  | 7.6440e-03  | 3.3800e-04  | 1.8800e-04  | 6.7704e-04  | 1.7540e-06 / 0.0000e+00",
    "   20 dB | 2.4814e-03  | 2.5020e-03  | 5.4000e-05  | 2.8000e-05  | 7.2564e-05  | 2.0370e-08 / 0.0000e+00",
    "   25 dB | 7.8870e-04  | 6.7400e-04  | 6.0000e-06  | 4.0000e-06  | 7.4216e-06  | 2.1384e-10 / 0.0000e+00",
    "--------------------------------------------------------------------------------------------------------",
    "PART 3: SHANNON CAPACITY & ERGODIC SPECTRAL EFFICIENCY (bps/Hz) AT KEY SNRs",
    "--------------------------------------------------------------------------------------------------------",
    " SNR(dB) | SISO AWGN   | SISO Rayl   | Fixed EPA   | Fixed WF    | Ergodic EPA | Ergodic WF  | Gain(WF-EPA)",
    "---------+-------------+-------------+-------------+-------------+-------------+-------------+-------------",
    "  -10 dB | 0.1375      | 0.1317      | 0.0776      | 0.1389      | 0.2630      | 0.4196      | +0.1566",
    "    0 dB | 1.0000      | 0.8602      | 0.6531      | 1.0079      | 1.6806      | 2.0750      | +0.3944",
    "   10 dB | 3.4594      | 2.9086      | 3.1293      | 3.4738      | 5.5411      | 5.7126      | +0.1715",
    "   20 dB | 6.6582      | 5.8880      | 8.1344      | 8.1465      | 11.2813     | 11.3077     | +0.0264",
    "   30 dB | 9.9672      | 9.1490      | 14.4925     | 14.4927     | 17.7334     | 17.7364     | +0.0029",
    "========================================================================================================",
    "[SIMULATION VERIFICATION COMPLETE] All 5 mathematical modules verified against analytical models."
]

renderTerminalImage(
    "tuong@workstation: ~/DoAn_2026/code/matlab — matlab -nodisplay",
    stbcLines,
    os.path.join(figuresDir, "term_capture_stbc_matlab.png")
)

renderTerminalImage(
    "tuong@workstation: ~/DoAn_2026/code/matlab — matlab -nodisplay",
    sdmLines,
    os.path.join(figuresDir, "term_capture_sdm_matlab.png")
)

renderTerminalImage(
    "tuong@workstation: ~/DoAn_2026 — python3 code/python/verify_all_simulations.py",
    summaryLines,
    os.path.join(figuresDir, "term_capture_simulation_summary.png")
)

print("Rendered all illustrated terminal images with exact monospace grid alignment.")
