<!-- ./docs/guide.md -->

# 开发者指南

> 本指南仅针对河南工业大学校园网有效，其他使用深澜的认证系统可参考本文，但不保证有效。

## 登录校园网

登录校园网需要对发送的用户名和密码进行加密，C语言示例：

```
/* 用户名加密 */
char stuno[]={"校园网账号"};//12位学号 
for (int i = 0; i < strlen(stuno); i++)
    stuno[i] += 4;
char username[22]={"{SRUN3}\r\n"};//总长为22位char
strcat(username,stuno);
```

```
/* 密码加密 */
char stupw[] = { "wwx123" };
char key[] = { "1234567890" };
const int len = 2 * strlen(stupw) + 1;
char* password = (char*) malloc(sizeof(char) * len);
memset(password, 0, len);
for (int i = 0; i < strlen(stupw); i++) {
    char ki = stupw[i] ^ key[10 - i % 10 - 1];
    char _l = (ki & 0x0f) + 0x36;
    char _h = (ki >> 4 & 0x0f) + 0x63;
    if (i % 2 == 0) {
        sprintf(password, "%s%c%c", password, _l, _h);
    }
    else {
        sprintf(password, "%s%c%c", password, _h, _l);
    }
}
```

```
/* 密码加密 */
char stupw[] = { "wwx123" };
char key[] = { "1234567890" };
const int len = 2 * strlen(stupw) + 1;
char* password = (char*) malloc(sizeof(char) * len);
memset(password, 0, len);
for (int i = 0; i < strlen(stupw); i++) {
    char ki = stupw[i] ^ key[10 - i % 10 - 1];
    char _l = (ki & 0x0f) + 0x36;
    char _h = (ki >> 4 & 0x0f) + 0x63;
    if (i % 2 == 0) {
        sprintf(password, "%s%c%c", password, _l, _h);
    }
    else {
        sprintf(password, "%s%c%c", password, _h, _l);
    }
}
```

加密完成后，向 `http://172.16.154.130:69/cgi-bin/srun_portal`

发送 `POST` 请求即可实现登录。

```
/* POST参数 */
Content-Type:application/x-www-form-urlencoded
Body:{
	"action": "login",
	"n": "117",
	"mbytes": "0",
	"minutes": "0",
	"ac_id": "1",
	"mac": "02:00:00:00:00:00",
	"type": "3",
	"username": username,
	"password": password,
	"drop": "0",
	"pop": "1"
    }
```

### TODO:

等待构建。
