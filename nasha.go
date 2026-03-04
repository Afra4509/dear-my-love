// nasha.go — dear-my-love · encrypted memory transmission
// Run : go run nasha.go
// Build: go build -o nasha.exe nasha.go

package main

import (
	"fmt"
	"os"
	"os/exec"
	"os/signal"
	"runtime"
	"strings"
	"syscall"
	"time"
)

// ════════════════════════════════════════════════════════════════════
//  ANSI ESCAPE CODES
// ════════════════════════════════════════════════════════════════════

const (
	RESET      = "\033[0m"
	BOLD       = "\033[1m"
	DIM        = "\033[2m"
	ITALIC     = "\033[3m"
	ERASE_LINE = "\033[2K"
	CURSOR_UP  = "\033[1A"
	HIDE_CURS  = "\033[?25l"
	SHOW_CURS  = "\033[?25h"

	// True-colour foreground  \033[38;2;R;G;Bm
	ROSE       = "\033[38;2;232;160;168m"
	ROSE_LIGHT = "\033[38;2;245;208;214m"
	ROSE_DARK  = "\033[38;2;194;89;106m"
	GOLD       = "\033[38;2;203;167;106m"
	GOLD_LIGHT = "\033[38;2;232;213;168m"
	TEXT_C     = "\033[38;2;212;184;190m"
	TEXT_DIM   = "\033[38;2;122;93;101m"
	CYAN       = "\033[38;2;126;207;207m"
	CYAN_DIM   = "\033[38;2;58;122;122m"
	GREEN      = "\033[38;2;126;207;158m"
	GREEN_DIM  = "\033[38;2;58;122;90m"
	GREY       = "\033[38;2;74;63;72m"
)

// ════════════════════════════════════════════════════════════════════
//  HELPERS
// ════════════════════════════════════════════════════════════════════

func enableVT() {
	if runtime.GOOS == "windows" {
		exec.Command("cmd", "/C", "chcp", "65001").Run() //nolint
	}
}

func ms(n int) { time.Sleep(time.Duration(n) * time.Millisecond) }

func center(s string, w int) string {
	r := []rune(s)
	if len(r) >= w {
		return s
	}
	pad := (w - len(r)) / 2
	return strings.Repeat(" ", pad) + s
}

// wrap wraps text to maxW runes, indented by indent spaces.
func wrap(text string, indent, maxW int) []string {
	words := strings.Fields(text)
	pfx := strings.Repeat(" ", indent)
	var lines []string
	line := pfx
	for _, w := range words {
		if len([]rune(line))+len([]rune(w))+1 > maxW {
			lines = append(lines, line)
			line = pfx + w + " "
		} else {
			line += w + " "
		}
	}
	if strings.TrimSpace(line) != "" {
		lines = append(lines, line)
	}
	return lines
}

func pline(col, s string) { fmt.Printf("%s%s%s\n", col, s, RESET) }
func dim(s string)        { pline(TEXT_DIM, s) }
func hr(col string, w int) {
	fmt.Printf("%s%s%s\n", col, strings.Repeat("─", w), RESET)
}

// ════════════════════════════════════════════════════════════════════
//  ASCII ART
// ════════════════════════════════════════════════════════════════════

var banner = []string{
	"  ██████╗     ███████╗    █████╗     ██████╗  ",
	"  ██╔══██╗    ██╔════╝   ██╔══██╗    ██╔══██╗ ",
	"  ██║  ██║    █████╗     ███████║    ██████╔╝ ",
	"  ██║  ██║    ██╔══╝     ██╔══██║    ██╔══██╗ ",
	"  ██████╔╝    ███████╗   ██║  ██║    ██║  ██║ ",
	"  ╚═════╝     ╚══════╝   ╚═╝  ╚═╝    ╚═╝  ╚═╝ ",
}

var heartBig = []string{
	" ████████  ████████ ",
	"████████████████████",
	"████████████████████",
	" ██████████████████ ",
	" ████████████████████",
	"  ████████████████  ",
	"   ██████████████   ",
	"     ██████████     ",
	"       ██████       ",
	"         ██         ",
}

var heartSmall = []string{
	"  ████  ████  ",
	" ████████████ ",
	" ████████████ ",
	"  ██████████  ",
	"   ████████   ",
	"    ██████    ",
	"      ██      ",
}

// ════════════════════════════════════════════════════════════════════
//  BOOT SEQUENCE
// ════════════════════════════════════════════════════════════════════

func bootSequence() {
	fmt.Print(HIDE_CURS)
	fmt.Println()

	grad := []string{ROSE_DARK, ROSE, ROSE_LIGHT, GOLD_LIGHT, ROSE_LIGHT, ROSE}
	for i, line := range banner {
		fmt.Printf("%s%s%s%s\n", BOLD+grad[i%len(grad)], center(line, 60), RESET, "")
		ms(75)
	}
	fmt.Println()

	dim("  ┌──────────────────────────────────────────────────────┐")
	dim("  │  DEAR-MY-LOVE  ·  v2.0  ·  encrypted transmission   │")
	dim("  └──────────────────────────────────────────────────────┘")
	fmt.Println()
	ms(300)

	logs := []struct{ col, msg string }{
		{GREEN_DIM, "[boot]   initializing memory encoder ..."},
		{GREEN_DIM, "[sys]    loading cryptographic identity module ..."},
		{CYAN_DIM, "[io]     mounting memory filesystem ..."},
		{CYAN_DIM, "[net]    establishing secure channel ..."},
		{GOLD, "[crypto] verifying recipient signature ..."},
		{ROSE_DARK, "[mem]    allocating heart buffer ..."},
		{ROSE, "[enc]    compiling emotional payload ..."},
		{GREEN, "[sys]    all systems nominal — transmission authorized"},
	}
	for _, l := range logs {
		pline(l.col, l.msg)
		ms(110)
	}
	fmt.Println()

	stages := []string{"BOOT", "LOAD", "INIT", "LINK"}
	for _, stage := range stages {
		for i := 0; i <= 32; i++ {
			bar := strings.Repeat("█", i) + strings.Repeat("░", 32-i)
			pct := i * 100 / 32
			fmt.Printf("\r%s  [%s]%s  [%s%s%s]  %3d%%", CYAN_DIM, stage, RESET, ROSE, bar, RESET, pct)
			ms(14)
		}
		fmt.Printf("  %s✓%s\n", GREEN, RESET)
	}
	fmt.Println()
	ms(400)
}

// ════════════════════════════════════════════════════════════════════
//  SYSTEM DASHBOARD
// ════════════════════════════════════════════════════════════════════

func systemDashboard() {
	dim("  ══════════════════════════════════════════════════════")
	pline(BOLD+GOLD, "  SYSTEM REPORT")
	dim("  ══════════════════════════════════════════════════════")
	fmt.Println()

	rows := []struct{ k, v, kc string }{
		{"OS", runtime.GOOS + " / " + runtime.GOARCH, CYAN_DIM},
		{"RUNTIME", "Go " + runtime.Version(), CYAN_DIM},
		{"CPUs", fmt.Sprintf("%d logical", runtime.NumCPU()), CYAN_DIM},
		{"SESSION", time.Now().Format("2006-01-02 15:04:05"), CYAN_DIM},
		{"RECIPIENT", "Nasha Putri Zaqirah", ROSE},
		{"SENDER", "Afra Fadma Dinata", ROSE},
		{"ENCODING", "UTF-8 / emotional-256", GOLD},
		{"STATUS", "AUTHORIZED  ✓", GREEN},
	}
	for _, r := range rows {
		fmt.Printf("  %s%-14s%s  %s│%s  %s%s%s\n",
			r.kc, r.k, RESET, TEXT_DIM, RESET, TEXT_C, r.v, RESET)
		ms(60)
	}
	fmt.Println()
	ms(400)
}

// ════════════════════════════════════════════════════════════════════
//  DECODE ANIMATION
// ════════════════════════════════════════════════════════════════════

func decodeAnimation() {
	dim("  ══════════════════════════════════════════════════════")
	pline(BOLD+ROSE_DARK, "  DECODING RECIPIENT SIGNATURE")
	dim("  ══════════════════════════════════════════════════════")
	fmt.Println()

	name := "Nasha Putri Zaqirah"

	// Hex dump
	fmt.Printf("%s  HEX_DUMP  »%s  ", CYAN_DIM, RESET)
	for _, b := range []byte(name) {
		fmt.Printf("%s%02X %s", CYAN, b, RESET)
		ms(35)
	}
	fmt.Println()

	// Binary (first 6 bytes only for brevity)
	fmt.Printf("%s  BINARY    »%s  ", CYAN_DIM, RESET)
	for _, b := range []byte(name[:6]) {
		fmt.Printf("%s%08b %s", GREEN_DIM, b, RESET)
		ms(45)
	}
	fmt.Printf("%s ...%s\n", TEXT_DIM, RESET)

	// Glitch reveal
	fmt.Println()
	noise := []rune("█▓▒░▒▓█")
	runes := []rune(name)
	for step := 0; step <= len(runes); step++ {
		revealed := string(runes[:step])
		glitch := ""
		for i := 0; i < len(runes)-step && i < 7; i++ {
			glitch += string(noise[i%len(noise)])
		}
		fmt.Printf("\r  %s%s%s%s%s%s    ", BOLD+ROSE, revealed, RESET, TEXT_DIM, glitch, RESET)
		ms(55)
	}
	fmt.Printf("\r  %s%s%s\n", BOLD+ROSE_LIGHT, name, RESET)
	fmt.Println()
	ms(500)
}

// ════════════════════════════════════════════════════════════════════
//  LETTER
// ════════════════════════════════════════════════════════════════════

type block struct{ tag, col, text string }

var letterBlocks = []block{
	{"INIT", CYAN_DIM, "Aku ingin memulai ini dengan jujur — bukan dengan kata yang dipoles, bukan dengan kalimat yang dilatih. Hanya aku, dan apa yang aku rasakan."},
	{"ADDR", ROSE_DARK, "Nasha. Namamu sendiri sudah terasa seperti sebuah baris kode yang, setiap kali aku baca, mengembalikan sesuatu yang hangat."},
	{"DATA", ROSE, "Aku tidak tahu persis kapan mulainya. Tapi aku tahu — ada momen-momen kecil bersamamu yang diam-diam aku simpan, seperti file yang tidak bisa aku hapus."},
	{"MEM_", GOLD, "Cara kamu tertawa. Cara kamu serius dengan hal-hal yang kamu pedulikan. Cara kamu hadir — bukan hanya secara fisik, tapi benar-benar hadir."},
	{"PROC", ROSE_LIGHT, "Dan aku, yang biasanya lebih nyaman dengan logika daripada perasaan, tiba-tiba mendapati diriku memikirkanmu lebih dari yang seharusnya."},
	{"SYNC", CYAN, "Bersamamu, aku tidak merasa perlu menjadi versi terbaik dari diriku. Aku cukup menjadi aku — dan itu rasanya seperti kebebasan."},
	{"EXEC", GREEN, "Aku tidak punya banyak janji besar. Yang aku punya hanyalah ini: aku ingin ada. Aku ingin mendengar. Aku ingin menjadi tempat yang aman bagimu."},
	{"SEND", GOLD_LIGHT, "Kalau kamu pernah merasa sendirian di tengah keramaian — aku ingin kamu tahu bahwa aku di sini. Dan aku tidak ke mana-mana."},
	{"RECV", ROSE, "Mungkin ini bukan waktu yang sempurna. Mungkin aku bukan orang yang sempurna. Tapi perasaan ini — ini nyata. Dan itu cukup bagiku untuk mengatakannya."},
	{"DONE", ROSE_DARK, "Jadi ini dia. Bukan akhir dari sesuatu, tapi awal — kalau kamu mau. Aku di sini, Nasha. Dan aku sangat ingin berada di sini, bersamamu."},
}

func renderLetter() {
	dim("  ══════════════════════════════════════════════════════")
	pline(BOLD+ROSE, "  TRANSMISSION PAYLOAD  ·  10 BLOCKS")
	dim("  ══════════════════════════════════════════════════════")
	fmt.Println()

	for i, b := range letterBlocks {
		fmt.Printf("%s  [%s] BLOCK_%02d%s\n", b.col, b.tag, i+1, RESET)
		for _, line := range wrap(b.text, 4, 70) {
			fmt.Printf("%s%s%s\n", TEXT_C, line, RESET)
			ms(7)
		}
		fmt.Println()
		ms(90)
	}
}

// ════════════════════════════════════════════════════════════════════
//  POEM
// ════════════════════════════════════════════════════════════════════

var poemLines = []struct{ col, text string }{
	{ROSE_LIGHT, "Namamu  ·  tiga suku kata"},
	{ROSE, "yang selalu aku ucapkan pelan-pelan"},
	{ROSE_LIGHT, "seolah kalau terlalu keras"},
	{GOLD_LIGHT, "ia akan hilang."},
	{TEXT_DIM, ""},
	{GOLD, "Kamu adalah jeda di antara baris kode"},
	{GOLD_LIGHT, "yang membuatnya masuk akal."},
	{TEXT_DIM, ""},
	{ROSE_LIGHT, "Dan aku — hanyalah seseorang"},
	{ROSE, "yang perlahan belajar"},
	{GOLD_LIGHT, "bahwa beberapa hal"},
	{ROSE_LIGHT, "tidak perlu dijelaskan."},
	{TEXT_DIM, ""},
	{ROSE, "Mereka cukup dirasakan."},
}

func renderPoem() {
	dim("  ══════════════════════════════════════════════════════")
	pline(BOLD+GOLD, "  POEM  ·  encoded in rose")
	dim("  ══════════════════════════════════════════════════════")
	fmt.Println()

	for _, l := range poemLines {
		if l.text == "" {
			fmt.Println()
		} else {
			pline(l.col, "    "+l.text)
		}
		ms(85)
	}
	fmt.Println()
	ms(300)
}

// ════════════════════════════════════════════════════════════════════
//  TRANSMISSION REPORT
// ════════════════════════════════════════════════════════════════════

func transmissionReport() {
	dim("  ══════════════════════════════════════════════════════")
	pline(BOLD+GREEN, "  TRANSMISSION REPORT")
	dim("  ══════════════════════════════════════════════════════")
	fmt.Println()

	rows := []struct{ k, v string }{
		{"BLOCKS_SENT", "10 / 10"},
		{"POEM_LINES", "14"},
		{"RECIPIENT", "Nasha Putri Zaqirah"},
		{"SENDER", "Afra Fadma Dinata"},
		{"TIMESTAMP", time.Now().Format("2006-01-02T15:04:05")},
		{"LANG", "Go " + runtime.Version()},
		{"STATUS", "DELIVERED  ✓"},
	}
	for _, r := range rows {
		fmt.Printf("  %s%-16s%s  %s%s%s\n", CYAN_DIM, r.k, RESET, GREEN, r.v, RESET)
		ms(80)
	}
	fmt.Println()
	ms(400)
}

// ════════════════════════════════════════════════════════════════════
//  OUTRO
// ════════════════════════════════════════════════════════════════════

func outro() {
	dim("  ══════════════════════════════════════════════════════")
	pline(BOLD+ROSE, "  END OF TRANSMISSION")
	dim("  ══════════════════════════════════════════════════════")
	fmt.Println()

	pline(BOLD+ITALIC+ROSE_LIGHT, center("Nasha Putri Zaqirah", 60))
	pline(TEXT_DIM, center("[ "+time.Now().Format("2006-01-02 15:04:05")+" ]", 60))
	fmt.Println()
	ms(600)
}

// ════════════════════════════════════════════════════════════════════
//  FINAL LOOP ANIMATION
// ════════════════════════════════════════════════════════════════════

var orbit = []rune("·  ✦  ·  ♡  ·  ✦  ·  ♡  ")
var waves = []string{
	"▁▂▃▄▅▆▇█▇▆▅▄▃▂▁",
	"▂▃▄▅▆▇█▇▆▅▄▃▂▁▂",
	"▃▄▅▆▇█▇▆▅▄▃▂▁▂▃",
	"▄▅▆▇█▇▆▅▄▃▂▁▂▃▄",
}
var roseCols = []string{ROSE_DARK, ROSE, ROSE_LIGHT, GOLD_LIGHT, GOLD, ROSE_LIGHT, ROSE}

func buildFrame(tick, W int, start time.Time) string {
	fps := 18
	big := (tick/fps)%2 == 0
	heart := heartSmall
	if big {
		heart = heartBig
	}
	hue := roseCols[tick%7]
	gCol := roseCols[tick%len(roseCols)]
	rCol := roseCols[tick%7]
	wCols := []string{CYAN_DIM, CYAN_DIM, ROSE_DARK, ROSE_DARK}
	wCol := wCols[tick%4]

	var sb strings.Builder

	sb.WriteString("\n")
	for _, line := range heart {
		sb.WriteString(fmt.Sprintf("%s%s%s\n", BOLD+hue, center(line, W), RESET))
	}

	sb.WriteString("\n")
	name := "Nasha Putri Zaqirah"
	sb.WriteString(fmt.Sprintf("%s%s%s\n", BOLD+ITALIC+gCol, center(name, W), RESET))

	sb.WriteString("\n")
	ringW := 48
	orbitStr := ""
	for i := 0; i < ringW; i++ {
		orbitStr += string(orbit[(tick+i)%len(orbit)])
	}
	sb.WriteString(fmt.Sprintf("%s%s%s\n", DIM+rCol, center(orbitStr, W), RESET))

	sb.WriteString("\n")
	wave := waves[tick%len(waves)]
	for len([]rune(wave)) < 40 {
		wave += waves[tick%len(waves)]
	}
	wave = string([]rune(wave)[:40])
	sb.WriteString(fmt.Sprintf("%s%s%s\n", DIM+wCol, center(wave, W), RESET))

	elapsed := time.Since(start)
	mins := int(elapsed.Minutes())
	secs := int(elapsed.Seconds()) % 60
	milli := int(elapsed.Milliseconds()) % 1000
	status := fmt.Sprintf("%s  looping  ·  %02d:%02d.%03d  ·  ctrl+c to exit",
		time.Now().Format("15:04:05"), mins, secs, milli)
	sb.WriteString(fmt.Sprintf("\n%s%s%s\n", DIM+GREY, center(status, W), RESET))

	return sb.String()
}

func finalLoop() {
	pline(TEXT_DIM, center("[ animation loop started — ctrl+c to exit ]", 60))
	fmt.Println()
	ms(600)

	sigs := make(chan os.Signal, 1)
	signal.Notify(sigs, syscall.SIGINT, syscall.SIGTERM)

	tick := 0
	fps := 18
	start := time.Now()
	W := 64

	// Count lines in first frame to know how many to erase
	frameLineCount := len(heartBig) + 9 // heart + extras
	firstFrame := true

	for {
		select {
		case <-sigs:
			fmt.Print(SHOW_CURS)
			fmt.Printf("\n%s  [ loop exited ✦ farewel, %s]%s\n\n", TEXT_DIM, "Nasha ", RESET)
			return
		default:
		}

		frame := buildFrame(tick, W, start)

		if !firstFrame {
			// Move cursor up past the previous frame
			for i := 0; i < frameLineCount; i++ {
				fmt.Print(CURSOR_UP + ERASE_LINE)
			}
		}
		firstFrame = false

		fmt.Print(frame)
		frameLineCount = strings.Count(frame, "\n")

		tick++
		time.Sleep(time.Second / time.Duration(fps))
	}
}

// ════════════════════════════════════════════════════════════════════
//  MAIN
// ════════════════════════════════════════════════════════════════════

func main() {
	enableVT()
	defer fmt.Print(SHOW_CURS)

	bootSequence()
	systemDashboard()
	decodeAnimation()
	renderLetter()
	renderPoem()
	transmissionReport()
	outro()
	finalLoop()
}
