import http from 'k6/http';
import { SharedArray } from 'k6/data';
import { check, sleep } from 'k6';

const endpoints = new SharedArray('endpoints', () =>
  JSON.parse(open('./merged-endpoints.json'))
);

export let options = {
  vus: endpoints.length,
  // iterations: endpoints.length,
  duration: '20s',
};

export default function () {
  const index = __VU - 1;
  const ep = endpoints[index];

  const res = http.get(ep.url);
  check(res, {
    [`[${ep.name}] status is 200`]: (r) => r.status === 200,
    [`[${ep.name}] body is not empty`]: (r) => r.body && r.body.length > 0,
  });

  // 💤 Add random sleep to stagger requests if using duration mode
  sleep(Math.random() * 2); // sleep 0–2 seconds
}