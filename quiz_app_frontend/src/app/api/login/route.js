// // pages/api/login.js
// export default async function handler(req, res) {
//   if (req.method !== 'POST') {
//     return res.status(405).json({ error: 'Method not allowed' });
//   }

//   const { token } = req.body;
//   if (!token) {
//     return res.status(400).json({ error: 'Token required' });
//   }


// }
export async function GET(request) {
  return new Response('Hello, Next.js!', {
    status: 200,
    headers: {
      'Access-Control-Allow-Origin': '*',
      'Access-Control-Allow-Methods': 'GET, POST, PUT, DELETE, OPTIONS',
      'Access-Control-Allow-Headers': 'Content-Type, Authorization',
    },
  })
}
export async function POST(request) {
  // Parse the request body (async operation)
  const { token } = await request.json();

  // Set the cookie in the headers
  const cookie = `access_token=${token}; HttpOnly; Secure=${process.env.NODE_ENV === 'production'}; SameSite=Strict; Path=/; Max-Age=3600`;
  
  return new Response("zale", {
    status: 200,
    headers: {
      'Set-Cookie': cookie, // Set the cookie here
      'Access-Control-Allow-Origin': 'http://192.168.43.88:3000', // Replace with your frontend origin
      'Access-Control-Allow-Methods': 'GET, POST, OPTIONS',
      'Access-Control-Allow-Headers': 'Content-Type, Authorization',
    },
  });
}