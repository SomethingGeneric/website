# pve1
IBM System X (something something) with latest Proxmox

## Container Services:
* `wazuh`: SEIM tool: `10.0.0.30`

## VM Services:
* `dockerboy`: Debian 12 host running Docker
    * Nginx Proxy Manager (to reverse-proxy hosted services): `10.0.0.26`
* `pihole`: Network DNS adblocker (installed on top of minimal Debian 12): `10.0.0.29`
* `wireguard`: VPN provider on top of Debian 12: `10.0.0.39`