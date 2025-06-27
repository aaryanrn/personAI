import type { NextApiRequest, NextApiResponse } from 'next';
import clientPromise from '@/lib/mongodb';
import { hash } from 'bcryptjs';

export default async function handler(req: NextApiRequest, res: NextApiResponse) {
  if (req.method !== 'POST') return res.status(405).end();

  const { email, password } = req.body;
  if (!email || !password) return res.status(400).json({ detail: 'Missing fields' });

  const client = await clientPromise;
  const db = client.db();
  const users = db.collection('users');

  const existing = await users.findOne({ email });
  if (existing) return res.status(400).json({ detail: 'Email already registered' });

  const hashed = await hash(password, 10);
  await users.insertOne({ email, password: hashed });

  res.status(201).json({ message: 'User created' });
}