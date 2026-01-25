#!/usr/bin/env python3
"""
Comprehensive Flask API to serve Boeing tweet data
Supports filtering by cluster, date range, country, sentiment, etc.
"""
from flask import Flask, request, jsonify
from flask_cors import CORS
import sqlite3
from datetime import datetime

app = Flask(__name__)
CORS(app)  # Enable CORS for frontend requests

DB_PATH = '/Users/angusmclean/Boeing/tweets_full.db'

def get_db_connection():
    """Get database connection"""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row  # Return rows as dictionaries
    return conn

@app.route('/api/tweets')
def get_tweets():
    """Get tweets with comprehensive filtering options"""
    # Filter parameters
    cluster = request.args.get('cluster')
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')
    country = request.args.get('country')
    sentiment = request.args.get('sentiment')
    emotion = request.args.get('emotion')
    min_impressions = request.args.get('min_impressions', type=int)
    
    # Pagination
    limit = request.args.get('limit', 50, type=int)  # Default 50 tweets
    offset = request.args.get('offset', 0, type=int)
    
    conn = get_db_connection()
    
    # Build query
    query = """
    SELECT date, title, snippet, author, impressions, reach, potential_audience,
           country, region, city, account_type, x_followers, x_likes, x_reposts,
           sentiment, emotion, gx_sentiment, gx_emotion, cluster, hashtags,
           engagement_score, impact
    FROM tweets
    """
    
    params = []
    conditions = []
    
    # Add filters
    if cluster:
        conditions.append("cluster = ?")
        params.append(cluster)
    
    if start_date:
        conditions.append("date >= ?")
        params.append(start_date)
    
    if end_date:
        conditions.append("date <= ?")
        params.append(end_date)
        
    if country:
        conditions.append("country = ?")
        params.append(country)
        
    if sentiment:
        conditions.append("gx_sentiment = ?")
        params.append(sentiment)
        
    if emotion:
        conditions.append("gx_emotion = ?")
        params.append(emotion)
        
    if min_impressions:
        conditions.append("impressions >= ?")
        params.append(min_impressions)
    
    if conditions:
        query += " WHERE " + " AND ".join(conditions)
    
    # Order by impressions (highest first) and add pagination
    query += " ORDER BY impressions DESC LIMIT ? OFFSET ?"
    params.extend([limit, offset])
    
    try:
        cursor = conn.execute(query, params)
        tweets = [dict(row) for row in cursor.fetchall()]
        
        # Get total count for pagination
        count_query = "SELECT COUNT(*) FROM tweets"
        count_params = params[:-2]  # Remove limit and offset
        
        if conditions:
            count_query += " WHERE " + " AND ".join(conditions)
            total = conn.execute(count_query, count_params).fetchone()[0]
        else:
            total = conn.execute("SELECT COUNT(*) FROM tweets").fetchone()[0]
        
        response = {
            'tweets': tweets,
            'total': total,
            'limit': limit,
            'offset': offset,
            'has_more': offset + len(tweets) < total
        }
        
        return jsonify(response)
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
    finally:
        conn.close()

@app.route('/api/clusters')
def get_clusters():
    """Get all available clusters with counts"""
    conn = get_db_connection()
    try:
        cursor = conn.execute("""
            SELECT cluster, COUNT(*) as count, 
                   AVG(impressions) as avg_impressions,
                   MAX(impressions) as max_impressions
            FROM tweets 
            GROUP BY cluster 
            ORDER BY count DESC
        """)
        clusters = [{
            'cluster': row['cluster'], 
            'count': row['count'],
            'avg_impressions': int(row['avg_impressions']),
            'max_impressions': row['max_impressions']
        } for row in cursor.fetchall()]
        return jsonify(clusters)
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        conn.close()

@app.route('/api/countries')
def get_countries():
    """Get all countries with tweet counts"""
    conn = get_db_connection()
    try:
        cursor = conn.execute("""
            SELECT country, COUNT(*) as count
            FROM tweets 
            WHERE country != 'Unknown'
            GROUP BY country 
            ORDER BY count DESC
            LIMIT 20
        """)
        countries = [dict(row) for row in cursor.fetchall()]
        return jsonify(countries)
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        conn.close()

@app.route('/api/stats')
def get_stats():
    """Get dataset statistics"""
    conn = get_db_connection()
    try:
        stats = {}
        
        # Basic counts
        stats['total_tweets'] = conn.execute('SELECT COUNT(*) FROM tweets').fetchone()[0]
        stats['unique_clusters'] = conn.execute('SELECT COUNT(DISTINCT cluster) FROM tweets').fetchone()[0]
        stats['unique_countries'] = conn.execute('SELECT COUNT(DISTINCT country) FROM tweets WHERE country != "Unknown"').fetchone()[0]
        stats['unique_authors'] = conn.execute('SELECT COUNT(DISTINCT author) FROM tweets WHERE author != "Unknown"').fetchone()[0]
        
        # Date range
        date_range = conn.execute('SELECT MIN(date) as min_date, MAX(date) as max_date FROM tweets').fetchone()
        stats['date_range'] = {'start': date_range['min_date'], 'end': date_range['max_date']}
        
        # Impression stats
        impression_stats = conn.execute('''
            SELECT MIN(impressions) as min_imp, MAX(impressions) as max_imp, 
                   AVG(impressions) as avg_imp, SUM(impressions) as total_imp
            FROM tweets
        ''').fetchone()
        stats['impressions'] = dict(impression_stats)
        
        # Sentiment distribution
        sentiment_dist = conn.execute('''
            SELECT gx_sentiment, COUNT(*) as count 
            FROM tweets 
            GROUP BY gx_sentiment
        ''').fetchall()
        stats['sentiment_distribution'] = {row['gx_sentiment']: row['count'] for row in sentiment_dist}
        
        return jsonify(stats)
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        conn.close()

@app.route('/api/health')
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'ok', 
        'message': 'Comprehensive Tweet API is running',
        'database': DB_PATH
    })

if __name__ == '__main__':
    print("Starting Comprehensive Tweet API server...")
    print(f"Database: {DB_PATH}")
    print("Available endpoints:")
    print("  GET /api/tweets - Get filtered tweets")
    print("  GET /api/clusters - Get cluster list") 
    print("  GET /api/countries - Get country list")
    print("  GET /api/stats - Get dataset statistics")
    print("  GET /api/health - Health check")
    
    app.run(debug=True, host='127.0.0.1', port=5000)