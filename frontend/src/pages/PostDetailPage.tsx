import { useParams } from 'react-router-dom'
import { useQuery } from 'react-query'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Badge } from '@/components/ui/badge'
import { Avatar, AvatarFallback, AvatarImage } from '@/components/ui/avatar'
import { Button } from '@/components/ui/button'
import { Textarea } from '@/components/ui/textarea'
import { Post, Comment } from '@/types'
import { formatDate, formatRelativeTime } from '@/lib/utils'
import { Eye, Heart, MessageCircle, Calendar, User, Send } from 'lucide-react'
import { useState } from 'react'
import { useAuth } from '@/contexts/AuthContext'
import api from '@/lib/api'
import ReactMarkdown from 'react-markdown'

export function PostDetailPage() {
  const { slug } = useParams<{ slug: string }>()
  const { user, isAuthenticated } = useAuth()
  const [commentText, setCommentText] = useState('')
  const [isSubmittingComment, setIsSubmittingComment] = useState(false)

  const { data: post, isLoading, error } = useQuery<Post>(
    ['post', slug],
    async () => {
      const response = await api.get(`/blog/posts/?slug=${slug}`)
      const posts = response.data.results || response.data
      return posts.find((p: Post) => p.slug === slug)
    }
  )

  const { data: comments, refetch: refetchComments } = useQuery<Comment[]>(
    ['comments', post?.id],
    async () => {
      if (!post) return []
      const response = await api.get(`/blog/posts/${post.id}/comments/`)
      return response.data
    },
    {
      enabled: !!post
    }
  )

  const handleLike = async () => {
    if (!post) return
    
    try {
      await api.post(`/blog/posts/${post.id}/like/`)
      // Refetch post data to update like count
      window.location.reload()
    } catch (error) {
      console.error('Error liking post:', error)
    }
  }

  const handleSubmitComment = async (e: React.FormEvent) => {
    e.preventDefault()
    if (!post || !commentText.trim() || !isAuthenticated) return

    setIsSubmittingComment(true)
    try {
      await api.post(`/blog/posts/${post.id}/comments/`, {
        content: commentText.trim()
      })
      setCommentText('')
      refetchComments()
    } catch (error) {
      console.error('Error submitting comment:', error)
    } finally {
      setIsSubmittingComment(false)
    }
  }

  if (isLoading) {
    return (
      <div className="max-w-4xl mx-auto">
        <Card className="animate-pulse">
          <CardHeader>
            <div className="h-8 bg-muted rounded w-3/4 mb-4"></div>
            <div className="h-4 bg-muted rounded w-1/2"></div>
          </CardHeader>
          <CardContent>
            <div className="space-y-4">
              <div className="h-4 bg-muted rounded"></div>
              <div className="h-4 bg-muted rounded w-5/6"></div>
              <div className="h-4 bg-muted rounded w-4/6"></div>
            </div>
          </CardContent>
        </Card>
      </div>
    )
  }

  if (error || !post) {
    return (
      <div className="max-w-4xl mx-auto text-center py-12">
        <h1 className="text-2xl font-bold mb-4">Post Not Found</h1>
        <p className="text-muted-foreground">The post you're looking for doesn't exist.</p>
      </div>
    )
  }

  return (
    <div className="max-w-4xl mx-auto space-y-8">
      {/* Post Content */}
      <article>
        <Card>
          <CardHeader>
            <div className="flex items-center justify-between mb-4">
              <div className="flex items-center space-x-3">
                <Avatar className="h-10 w-10">
                  <AvatarImage src={post.author.avatar} alt={post.author.username} />
                  <AvatarFallback>
                    {post.author.username.charAt(0).toUpperCase()}
                  </AvatarFallback>
                </Avatar>
                <div>
                  <p className="font-medium">{post.author.username}</p>
                  <p className="text-sm text-muted-foreground">
                    {formatDate(post.published_at || post.created_at)}
                  </p>
                </div>
              </div>
              <div className="flex items-center space-x-2">
                <Button variant="outline" size="sm" onClick={handleLike}>
                  <Heart className="h-4 w-4 mr-2" />
                  {post.like_count}
                </Button>
              </div>
            </div>

            <CardTitle className="text-3xl mb-4">{post.title}</CardTitle>
            
            {post.excerpt && (
              <CardDescription className="text-lg">
                {post.excerpt}
              </CardDescription>
            )}

            {/* Tags */}
            {post.tags.length > 0 && (
              <div className="flex flex-wrap gap-2 mt-4">
                {post.tags.map((tag) => (
                  <Badge key={tag.id} variant="secondary">
                    {tag.name}
                  </Badge>
                ))}
              </div>
            )}
          </CardHeader>

          <CardContent>
            {post.featured_image && (
              <div className="mb-8">
                <img
                  src={post.featured_image}
                  alt={post.title}
                  className="w-full h-auto rounded-lg"
                />
              </div>
            )}

            <div className="prose prose-lg max-w-none">
              <ReactMarkdown>{post.content || ''}</ReactMarkdown>
            </div>

            {/* Post Stats */}
            <div className="flex items-center justify-between mt-8 pt-8 border-t">
              <div className="flex items-center space-x-6 text-sm text-muted-foreground">
                <div className="flex items-center space-x-1">
                  <Eye className="h-4 w-4" />
                  <span>{post.view_count} views</span>
                </div>
                <div className="flex items-center space-x-1">
                  <Heart className="h-4 w-4" />
                  <span>{post.like_count} likes</span>
                </div>
                <div className="flex items-center space-x-1">
                  <MessageCircle className="h-4 w-4" />
                  <span>{post.comment_count} comments</span>
                </div>
              </div>
            </div>
          </CardContent>
        </Card>
      </article>

      {/* Comments Section */}
      {post.allow_comments && (
        <section>
          <h2 className="text-2xl font-bold mb-6">Comments</h2>
          
          {/* Comment Form */}
          {isAuthenticated ? (
            <Card className="mb-6">
              <CardContent className="pt-6">
                <form onSubmit={handleSubmitComment} className="space-y-4">
                  <div>
                    <Textarea
                      placeholder="Write a comment..."
                      value={commentText}
                      onChange={(e) => setCommentText(e.target.value)}
                      rows={4}
                    />
                  </div>
                  <div className="flex justify-end">
                    <Button 
                      type="submit" 
                      disabled={!commentText.trim() || isSubmittingComment}
                    >
                      <Send className="h-4 w-4 mr-2" />
                      {isSubmittingComment ? 'Posting...' : 'Post Comment'}
                    </Button>
                  </div>
                </form>
              </CardContent>
            </Card>
          ) : (
            <Card className="mb-6">
              <CardContent className="pt-6 text-center">
                <p className="text-muted-foreground">
                  Please log in to leave a comment.
                </p>
              </CardContent>
            </Card>
          )}

          {/* Comments List */}
          <div className="space-y-4">
            {comments?.map((comment) => (
              <Card key={comment.id}>
                <CardContent className="pt-6">
                  <div className="flex items-start space-x-3">
                    <Avatar className="h-8 w-8">
                      <AvatarImage src={comment.author.avatar} alt={comment.author.username} />
                      <AvatarFallback>
                        {comment.author.username.charAt(0).toUpperCase()}
                      </AvatarFallback>
                    </Avatar>
                    <div className="flex-1">
                      <div className="flex items-center space-x-2 mb-2">
                        <span className="font-medium text-sm">{comment.author.username}</span>
                        <span className="text-xs text-muted-foreground">
                          {formatRelativeTime(comment.created_at)}
                        </span>
                      </div>
                      <p className="text-sm whitespace-pre-wrap">{comment.content}</p>
                    </div>
                  </div>
                </CardContent>
              </Card>
            ))}

            {comments?.length === 0 && (
              <Card>
                <CardContent className="pt-6 text-center">
                  <p className="text-muted-foreground">No comments yet. Be the first to comment!</p>
                </CardContent>
              </Card>
            )}
          </div>
        </section>
      )}
    </div>
  )
}
