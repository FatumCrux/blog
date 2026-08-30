// 后端返回的时间格式是 ISO 8601 格式的字符串，用JS将其格式化为更易读的形式。
export function formatDate(isoString){
    const date = new Date(isoString)  // 创建一个 Date 对象，自动转为本地时区
    const pad = (n) => n.toString().padStart(2, '0')  // 补零函数
    const year = date.getFullYear() 
    const month = pad(date.getMonth() + 1)  // 月份从0开始
    const day = pad(date.getDate())
    const hours = pad(date.getHours())
    const minutes = pad(date.getMinutes())
    const seconds = pad(date.getSeconds())
    return `${year}-${month}-${day} ${hours}:${minutes}:${seconds}`
}