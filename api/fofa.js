export const config = {
  runtime: 'edge',
};

export default async function handler(req) {
  if (req.method !== 'POST') {
    return new Response('Only POST allowed', { status: 405 });
  }

  const body = await req.formData();
  const query = body.get('query');
  const email = process.env.FOFA_EMAIL;
  const key = process.env.FOFA_KEY;

  const qbase64 = btoa(query);
  const url = `https://fofa.info/api/v1/search/all?email=${email}&key=${key}&qbase64=${qbase64}&size=50`;

  try {
    const resp = await fetch(url);
    const json = await resp.json();
    return Response.json(json);
  } catch (e) {
    return new Response(JSON.stringify({ error: e.message }), { status: 500 });
  }
}
