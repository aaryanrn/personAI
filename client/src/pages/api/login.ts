import type { NextApiRequest, NextApiResponse } from 'next';
import clientPromise from '@/lib/mongodb';
import { compare } from 'bcryptjs';

export default async function handler(req: NextApiRequest, res: NextApiResponse) {
  if (req.method !== 'POST') return res.status(405).end();

  const { email, password } = req.body;
  if (!email || !password) return res.status(400).json({ detail: 'Missing fields' });

  const client = await clientPromise;
  const db = client.db();
  const users = db.collection('users');

  const user = await users.findOne({ email });
  if (!user) return res.status(401).json({ detail: 'Invalid email or password' });

  const valid = await compare(password, user.password);
  if (!valid) return res.status(401).json({ detail: 'Invalid email or password' });

  res.status(200).json({ message: 'Login successful' });
}