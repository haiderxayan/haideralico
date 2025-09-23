---
layout: page
title: Reading
permalink: /reading/
---

# What I'm Reading

A curated collection of books, articles, and resources that inspire my design thinking and professional growth.

## Latest Reading Insights

{% for post in site.posts %}
{% if post.categories contains 'Reading' %}
<div class="reading-post">
  <h3><a href="{{ post.url }}">{{ post.title }}</a></h3>
  <div class="post-meta">
    <span class="post-date">{{ post.date | date: "%B %d, %Y" }}</span>
    <span class="read-time">{{ post.read_time }} min read</span>
  </div>
  <p class="post-excerpt">{{ post.excerpt }}</p>
  <a href="{{ post.url }}" class="read-more">Read more →</a>
</div>
{% endif %}
{% endfor %}

## Design & UX Favorites

### "Don't Make Me Think" by Steve Krug
*The classic guide to web usability that every designer should read.*

### "The Elements of User Experience" by Jesse James Garrett
*A comprehensive framework for understanding and implementing user experience design.*

### "About Face" by Alan Cooper
*Essential reading for interaction design and user-centered design methodologies.*

### "Hooked" by Nir Eyal
*Understanding how to build products that create lasting user engagement.*

## Business & Strategy

### "Good to Great" by Jim Collins
*What makes companies transition from good to great performance.*

### "Crossing the Chasm" by Geoffrey Moore
*Marketing and selling disruptive products to mainstream customers.*

### "The Innovator's Dilemma" by Clayton Christensen
*Understanding disruptive innovation and its impact on established companies.*

## Psychology & Human Behavior

### "Influence" by Robert Cialdini
*The psychology of persuasion and how it applies to design and user experience.*

### "Predictably Irrational" by Dan Ariely
*Understanding the hidden forces that shape our decisions.*

### "Nudge" by Richard Thaler
*How small changes in choice architecture can lead to better decisions.*

## Articles & Resources

### Design Blogs I Follow
- [Nielsen Norman Group](https://www.nngroup.com/) - Evidence-based UX research
- [UX Planet](https://uxplanet.org/) - Community-driven design insights
- [Smashing Magazine](https://www.smashingmagazine.com/) - Web design and development
- [A List Apart](https://alistapart.com/) - Web standards and best practices

### Newsletters
- **UX Weekly** - Curated UX articles and resources
- **Designer Hangout** - Community insights and job opportunities
- **The UX Newsletter** - Latest trends and case studies

## Reading Goals for 2024

- [ ] "The Mom Test" by Rob Fitzpatrick
- [ ] "Continuous Discovery Habits" by Teresa Torres
- [ ] "Escaping the Build Trap" by Melissa Perri
- [ ] "User Story Mapping" by Jeff Patton
- [ ] "The Lean Product Playbook" by Dan Olsen

## Book Recommendations

Have a book recommendation for me? I'm always looking for new perspectives on design, business, and human behavior. Feel free to [reach out](/contact/) with your suggestions!

---

*"The more that you read, the more things you will know. The more that you learn, the more places you'll go."* - Dr. Seuss
