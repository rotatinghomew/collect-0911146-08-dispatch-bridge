# 物流商接入约定

CallbackProbe 目前只验证和回显通知，不承诺持久接收；tracking_client 只提供独立详情和活跃运单查询。
演练密钥均为公开的本地测试值。HMAC-SHA256 的待签字节为十进制时间戳 + '.' + 原始请求体。
X-Tenant、X-Key-Id 选择密钥，X-Timestamp 有 300 秒时间窗，X-Signature 用十六进制表示。
通知内容有 tenant、delivery、shipment、revision，可只有 hint=true，也可有 status 与 retracts。
delivery 只标识一次投递；不同投递可能声明同一业务修订，重复投递的正文也要比较。
运单业务主键含 tenant，同号运单可属于不同租户。revision 为单运单递增修订，不是所有通知的全局序号。
详情可能暂时落后于通知，或者与同修订通知冲突。retracted 要指向被撤回修订，不能简单当成 delivered 的更新时间。
/active 返回仍需覆盖的业务对象；没有通知不代表已经终结。Provider.budget 控制实际详情查询次数。
