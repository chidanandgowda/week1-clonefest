export interface User {
  id: number
  username: string
  email: string
  first_name: string
  last_name: string
  bio?: string
  avatar?: string
  website?: string
  location?: string
  birth_date?: string
  is_verified: boolean
  date_joined: string
  last_login?: string
}

export interface Category {
  id: number
  name: string
  slug: string
  description?: string
  color: string
  created_at: string
}

export interface Tag {
  id: number
  name: string
  slug: string
  created_at: string
}

export interface Comment {
  id: number
  author: User
  content: string
  parent?: number
  replies: Comment[]
  created_at: string
  updated_at: string
}

export interface Post {
  id: number
  title: string
  slug: string
  content?: string
  excerpt?: string
  author: User
  category?: Category
  tags: Tag[]
  status: 'draft' | 'published' | 'archived'
  featured_image?: string
  view_count: number
  like_count: number
  comment_count: number
  is_featured: boolean
  allow_comments: boolean
  created_at: string
  updated_at: string
  published_at?: string
  comments?: Comment[]
}

export interface FeatherType {
  id: number
  name: string
  slug: string
  description?: string
  icon: string
  is_active: boolean
  created_at: string
}

export interface TextFeather {
  id: number
  content: string
  format: 'plain' | 'markdown' | 'html'
  created_at: string
  updated_at: string
}

export interface PhotoFeather {
  id: number
  image: string
  caption?: string
  alt_text?: string
  width?: number
  height?: number
  created_at: string
  updated_at: string
}

export interface QuoteFeather {
  id: number
  quote: string
  author?: string
  source?: string
  created_at: string
  updated_at: string
}

export interface LinkFeather {
  id: number
  url: string
  title?: string
  description?: string
  thumbnail?: string
  created_at: string
  updated_at: string
}

export interface VideoFeather {
  id: number
  video_file?: string
  video_url?: string
  thumbnail?: string
  caption?: string
  duration?: string
  created_at: string
  updated_at: string
}

export interface AudioFeather {
  id: number
  audio_file: string
  title?: string
  artist?: string
  duration?: string
  created_at: string
  updated_at: string
}

export interface UploadedFile {
  id: number
  file: string
  original_name: string
  file_size: number
  file_size_human: string
  mime_type: string
  uploaded_at: string
}

export interface UploaderFeather {
  id: number
  files: UploadedFile[]
  description?: string
  created_at: string
  updated_at: string
}

export interface Theme {
  id: number
  name: string
  slug: string
  description?: string
  author?: string
  version: string
  is_active: boolean
  is_default: boolean
  css_file?: string
  preview_image?: string
  created_at: string
  updated_at: string
}

export interface LoginCredentials {
  username: string
  password: string
}

export interface RegisterData {
  username: string
  email: string
  first_name: string
  last_name: string
  password: string
  password_confirm: string
}

export interface AuthResponse {
  user: User
  tokens: {
    access: string
    refresh: string
  }
}
