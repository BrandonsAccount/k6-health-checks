import http from 'k6/http';
import { SharedArray } from 'k6/data';
import { check, sleep } from 'k6';

const endpoints = new SharedArray('endpoints', () =>
  JSON.parse(open('./merged-endpoints.json'))
);

export let options = {
  scenarios: {
    forever: {
      executor: 'constant-vus',
      vus: endpoints.length,
      duration: '10000h', // you need duration in order to have multimple VUs. An infinite duration will not work.
    },
  },
};

export default function () {
  const index = __VU - 1;
  const ep = endpoints[index];

  console.log(`[VU ${__VU}] hitting ${ep.url}`);

  // Use the endpoint name as a tag for better observability
  const tags = {
    endpoint_name: ep.name || `ep-${__VU}`,
    endpoint_url: ep.url,
  };

  const res = http.get(ep.url, { tags });

  // perform the health checks
  check(res, {
    [`[${ep.name}] status is 200`]: (r) => r.status === 200,
    [`[${ep.name}] body is not empty`]: (r) => r.body && r.body.length > 0,
  });

  // 💤 Add random sleep to stagger requests if using duration mode
  sleep(Math.random() * 2); // sleep 0–2 seconds
}