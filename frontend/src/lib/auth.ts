import { api } from './api'
import type { User } from '@/types'

export async function login(email: string, password: string): Promise<string> {
  const data = await api.post<{ access_token: string }>('/api/auth/login', { email, password })
  localStorage.setItem('access_token', data.access_token)
  return data.access_token
}

export async function logout(): Promise<void> {
  await api.post('/api/auth/logout', {}).catch(() => {})
  localStorage.removeItem('access_token')
}

export async function getMe(): Promise<User> {
  return api.get<User>('/api/auth/me')
}
