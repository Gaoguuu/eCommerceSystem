import axios from 'axios'

export function getTableList(param) {
  return axios({
    url: 'https://cdn.jsdelivr.net/gh/baimingxuan/media-store/mock-data/table-list.json',
    method: 'get',
    param
  })
}
export const mrpOpera = data => {
  return axios.post("/api/mrp", data).then(res => res.data);
};
