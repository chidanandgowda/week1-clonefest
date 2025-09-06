import { useQuery } from 'react-query'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Badge } from '@/components/ui/badge'
import { Avatar, AvatarFallback, AvatarImage } from '@/components/ui/avatar'
import { Button } from '@/components/ui/button'
import { useAuth } from '@/contexts/AuthContext'
import { formatDate } from '@/lib/utils'
import { User, Calendar, Mail, Globe, MapPin, Edit } from 'lucide-react'
import { Link } from 'react-router-dom'
import api from '@/lib/api'

export function ProfilePage() {
  const { user, isAuthenticated } = useAuth()

  const { data: userPosts } = useQuery(
    ['user-posts', user?.id],
    async () => {
      if (!user) return []
      const response = await api.get(`/blog/posts/?author=${user.username}`)
      return response.data.results || response.data
    },
    {
      enabled: !!user
    }
  )

  if (!isAuthenticated || !user) {
    return (
      <div className="max-w-4xl mx-auto text-center py-12">
        <h1 className="text-2xl font-bold mb-4">Please log in</h1>
        <p className="text-muted-foreground">You need to be logged in to view your profile.</p>
      </div>
    )
  }

  return (
    <div className="max-w-4xl mx-auto space-y-8">
      {/* Profile Header */}
      <Card>
        <CardContent className="pt-6">
          <div className="flex flex-col md:flex-row items-start md:items-center space-y-4 md:space-y-0 md:space-x-6">
            <Avatar className="h-24 w-24">
              <AvatarImage src={user.avatar} alt={user.username} />
              <AvatarFallback className="text-2xl">
                {user.username.charAt(0).toUpperCase()}
              </AvatarFallback>
            </Avatar>
            
            <div className="flex-1">
              <div className="flex items-center space-x-2 mb-2">
                <h1 className="text-3xl font-bold">{user.username}</h1>
                {user.is_verified && (
                  <Badge variant="secondary">Verified</Badge>
                )}
              </div>
              
              {user.first_name && user.last_name && (
                <p className="text-lg text-muted-foreground mb-2">
                  {user.first_name} {user.last_name}
                </p>
              )}
              
              {user.bio && (
                <p className="text-muted-foreground mb-4">{user.bio}</p>
              )}
              
              <div className="flex flex-wrap gap-4 text-sm text-muted-foreground">
                <div className="flex items-center space-x-1">
                  <Calendar className="h-4 w-4" />
                  <span>Joined {formatDate(user.date_joined)}</span>
                </div>
                {user.email && (
                  <div className="flex items-center space-x-1">
                    <Mail className="h-4 w-4" />
                    <span>{user.email}</span>
                  </div>
                )}
                {user.website && (
                  <div className="flex items-center space-x-1">
                    <Globe className="h-4 w-4" />
                    <a 
                      href={user.website} 
                      target="_blank" 
                      rel="noopener noreferrer"
                      className="hover:text-primary transition-colors"
                    >
                      Website
                    </a>
                  </div>
                )}
                {user.location && (
                  <div className="flex items-center space-x-1">
                    <MapPin className="h-4 w-4" />
                    <span>{user.location}</span>
                  </div>
                )}
              </div>
            </div>
            
            <Button variant="outline" size="sm">
              <Edit className="h-4 w-4 mr-2" />
              Edit Profile
            </Button>
          </div>
        </CardContent>
      </Card>

      {/* User Posts */}
      <section>
        <div className="flex items-center justify-between mb-6">
          <h2 className="text-2xl font-bold">My Posts</h2>
          <Button asChild>
            <Link to="/create">
              Create New Post
            </Link>
          </Button>
        </div>

        {userPosts?.length === 0 ? (
          <Card>
            <CardContent className="pt-6 text-center">
              <p className="text-muted-foreground mb-4">You haven't written any posts yet.</p>
              <Button asChild>
                <Link to="/create">Create your first post</Link>
              </Button>
            </CardContent>
          </Card>
        ) : (
          <div className="grid gap-6 md:grid-cols-2">
            {userPosts?.map((post) => (
              <Card key={post.id} className="overflow-hidden hover:shadow-lg transition-shadow">
                {post.featured_image && (
                  <div className="aspect-video overflow-hidden">
                    <img
                      src={post.featured_image}
                      alt={post.title}
                      className="w-full h-full object-cover"
                    />
                  </div>
                )}
                <CardHeader>
                  <div className="flex items-center justify-between mb-2">
                    <Badge variant={post.status === 'published' ? 'default' : 'secondary'}>
                      {post.status}
                    </Badge>
                    <span className="text-sm text-muted-foreground">
                      {formatDate(post.created_at)}
                    </span>
                  </div>
                  <CardTitle className="line-clamp-2">
                    <Link to={`/post/${post.slug}`} className="hover:text-primary transition-colors">
                      {post.title}
                    </Link>
                  </CardTitle>
                  <CardDescription className="line-clamp-3">
                    {post.excerpt || post.content?.substring(0, 150) + '...'}
                  </CardDescription>
                </CardHeader>
                <CardContent>
                  <div className="flex items-center justify-between text-sm text-muted-foreground">
                    <div className="flex items-center space-x-4">
                      <span>{post.view_count} views</span>
                      <span>{post.like_count} likes</span>
                      <span>{post.comment_count} comments</span>
                    </div>
                    <Button variant="ghost" size="sm" asChild>
                      <Link to={`/post/${post.slug}`}>
                        Read More
                      </Link>
                    </Button>
                  </div>
                </CardContent>
              </Card>
            ))}
          </div>
        )}
      </section>
    </div>
  )
}
