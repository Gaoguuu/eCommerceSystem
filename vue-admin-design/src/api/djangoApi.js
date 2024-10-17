/**
 * 程序名：api接口
 * 功能：与后端通讯的api接口定义
 */
import axios from "axios";

export const mrpOpera = data => {
  return axios.post("/api/mrp", data).then(res => res.data);
};