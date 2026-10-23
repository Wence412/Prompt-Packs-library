# 🤝 Contributing to ChatGPT-Image Prompt Packs

Thank you for helping us build the most comprehensive AI image prompt library! Your contributions make this resource more valuable for everyone.

## 🎯 Contribution Types

We welcome contributions in these areas:

| Type | Description | Effort |
|------|-------------|--------|
| 📝 **New Prompts** | Add production-ready prompts following the S.E.E.D. framework | ⭐⭐ |
| 🐛 **Bug Fixes** | Correct errors, formatting, or placeholder issues | ⭐ |
| 📚 **Documentation** | Improve guides, examples, or workflows | ⭐⭐ |
| 🎨 **Templates** | Create universal templates for new use cases | ⭐⭐⭐ |
| ✨ **Improvements** | Optimize existing prompts or add variations | ⭐⭐ |
| 🔍 **Quality Review** | Test prompts and provide feedback | ⭐ |

---

## 📋 Before You Start

✅ **Do:**
- Follow the [S.E.E.D. Framework](seed-framework.md)
- Test your prompts in a supported GPT Image workflow
- Use the production checklist before submitting
- Provide real-world use cases
- Document winning variations
- Include relevant tags for categorization

❌ **Don't:**
- Request real-person likenesses without explicit permission
- Include copyrighted characters or logos
- Generate prompts for harmful use cases
- Submit untested or vague prompts
- Duplicate existing prompts without improvements
- Add random text or unvalidated output

---

## 🚀 Quick Start: Adding a New Prompt

### Step 1: Set Up Your Fork
```bash
# Fork the repo on GitHub
# Clone your fork
git clone https://github.com/YOUR_USERNAME/chatgpt-image-prompt-packs.git
cd chatgpt-image-prompt-packs

# Create a new branch
git checkout -b add/your-prompt-name
```

### Step 2: Create Your Prompt
Use the S.E.E.D. framework:

```text
Subject: [What is the hero?]
Elements: [Props, colors, materials?]
Environment: [Where is this taking place?]
Details: [Lens, lighting, style, constraints?]
Production line: [Quality standards and output requirements?]
```

**Example:**
```
Create a premium studio mockup of [product] for [brand] on a clean matte surface 
with soft shadows, elegant reflections, and a minimalist background in [color palette]. 
Use commercial-grade lighting, realistic product proportions, accurate materials, 
depth of field, no random text, and brand-safe visual treatment. Output should be 
clean, polished, and ready for web/print without editing.
```

### Step 3: Test Your Prompt
```bash
# Generate or edit the image in a supported GPT Image workflow
# Rate the output quality
# Note any variations or refinements
# Document the winning version
```

### Step 4: Add to `prompts.json`

```json
{
  "id": "P1-XXX",
  "phase": "Phase 1",
  "category": "Your Category",
  "title": "Your Prompt Title",
  "prompt": "Your full S.E.E.D. prompt text here...",
  "best_for": "Visual ideation, product concepts, [your use case]",
  "framework": "Subject + context + style + environment + materials + camera/framing + lighting + brand constraints + output format",
  "tags": [
    "category-tag",
    "specific-prompt-tag",
    "chatgpt-image-2",
    "commercial-use"
  ]
}
```

### Step 5: Update `categories.json`

If adding to a new category:

```json
"Your New Category": [
  "P1-XXX",
  "P1-YYY"
]
```

### Step 6: Rebuild exports and validate

```bash
python3 scripts/build_exports.py
python3 scripts/validate.py
```

### Step 7: Create a Pull Request

```bash
# Commit your changes
git add prompts.json categories.json prompts.csv chatgpt-image-prompt-library.import.json
git commit -m "Add P1-XXX: Your Prompt Title"

# Push to your fork
git push origin add/your-prompt-name

# Create PR on GitHub with:
# Title: "Add P1-XXX: Your Prompt Title"
# Description: Explain the use case and why it's valuable
```

---

## 📐 Prompt Format Guidelines

### Required Fields

```json
{
  "id": "P[PHASE]-[NUMBER]",           // P1-001, P2-050, etc.
  "phase": "Phase 1 or Phase 2",        // Clearly labeled
  "category": "Existing Category",      // Must match categories.json
  "title": "Clear, Descriptive Title",  // 3-5 words
  "prompt": "Full S.E.E.D. prompt...",  // Direct and specific, without filler
  "best_for": "Use case 1, Use case 2", // Why use this?
  "framework": "S.E.E.D. components",   // How it's structured
  "tags": ["tag1", "tag2"]              // Min 3, Max 8 tags
}
```

### ID Numbering

- **Phase 1:** P1-001 through P1-075
- **Phase 2:** P2-001 through P2-095
- **New prompts:** Use the next available number in your phase

### Category Mapping

**Phase 1 Categories:**
- Product Mockups
- Product Design Concepts
- Packaging Design
- Brand Identity and Campaign Visuals
- UI, App, and Digital Product Prompts
- Advertising and Social Content
- Editorial, Commercial, and Lifestyle Scenes
- Product Visualization and Explainers
- Advanced Creative Direction

**Phase 2 Categories:**
- Virtual Brand Ambassadors and AI Influencers
- Commercial Asset Bundles
- Automated Print-on-Demand Designs
- Ad Creative Optimization
- Photorealistic Business and Lifestyle
- Product-Focused E-Commerce and Mockups
- Brand-Stylized Visual Systems
- High-Concept, Entertainment, and Storytelling
- Brand Consistency and Visual Systems
- Bonus Production Prompts for Service Packages

### Tags Best Practices

Use tags for discoverability:
- **Format:** lowercase, hyphen-separated
- **Examples:** `product-mockups`, `ai-influencer`, `chatgpt-image-2`
- **Minimum 3 tags**
- Always include: `chatgpt-image-2`, `commercial-use` (or similar)

---

## ✅ Quality Checklist

Before submitting, verify:

- [ ] Prompt is production-ready (tested in a supported GPT Image workflow)
- [ ] Follows S.E.E.D. framework structure
- [ ] Uses clear placeholder variables: `[product]`, `[brand]`, `[audience]`, etc.
- [ ] No copyrighted characters, real logos, or real-person likenesses
- [ ] No random generated text or unvalidated elements
- [ ] Clear and specific output requirements
- [ ] Prompt length fits the use case and includes only necessary direction
- [ ] Best_for and tags are accurate
- [ ] JSON is properly formatted (valid syntax)
- [ ] Doesn't duplicate existing prompts without significant improvement
- [ ] Real-world use case clearly explained

---

## 🎨 Improvement Suggestions

### Enhancing Existing Prompts

If you want to improve an existing prompt:

1. Test the current version
2. Identify what's missing (clarity, specificity, constraints)
3. Create an improved version using S.E.E.D.
4. Submit a PR with:
   - Original prompt ID
   - Reason for improvement
   - Testing results
   - Before/after comparison

### Adding Variations

Create variations for different use cases:
- **Same prompt, different style** (e.g., luxury vs. casual)
- **Same concept, different platform** (e.g., Instagram vs. email)
- **Same objective, different emotion** (e.g., calm vs. energetic)

Label with a suffix: `P1-001-v2`, `P1-001-luxury`, etc.

---

## 🐛 Reporting Issues

Found a problem?

**Bug Report Template:**

```markdown
## Issue Title
[Clear, specific title]

## Description
[What's wrong?]

## Steps to Reproduce
1. [Used prompt ID]
2. [Specific variables tested]
3. [ChatGPT-Image settings]

## Expected vs. Actual
Expected: [What should happen]
Actual: [What actually happened]

## Attachment
[Screenshot or output image if applicable]
```

**Quick Issues:**
- Typos or formatting errors
- Broken placeholders
- Invalid JSON syntax
- Missing or incorrect metadata

---

## 💬 Discussion & Ideas

Have an idea but not ready to contribute code?

1. **Start a Discussion:** Share your prompt concept
2. **Get Feedback:** Community can help refine it
3. **Collaborate:** Work with others to perfect it
4. **Submit Together:** Create a polished PR

---

## 🏆 Recognition

Contributors are recognized in:
- **CHANGELOG.md** – Major contributions listed by version
- **README.md** – Featured contributors section (coming soon)
- **GitHub Contributors** – Automatically tracked

---

## 📖 Additional Resources

- [S.E.E.D. Framework](seed-framework.md) – How to structure prompts
- [Production Checklist](production-checklist.md) – Quality standards
- [Before & After Workflow](before-after-workflow.md) – Prompt evolution
- [Ad Testing Matrix](ad-testing-matrix.md) – Testing methodology
- [Prompt schema](schema/prompt-card-v2.schema.json) – Data format reference

---

## ❓ FAQ

**Q: Can I contribute prompts for other AI image tools?**
A: This library is optimized for GPT Image workflows. Open a discussion before adding another platform so capability and licensing guidance can remain clear.

**Q: What if my prompt doesn't get accepted?**
A: We'll provide constructive feedback. You can refine and resubmit. Rejection reasons include: untested, vague, duplicative, or off-brand.

**Q: How often are contributions reviewed?**
A: We review PRs weekly. Major additions take 3-7 days; small fixes are quicker.

**Q: Can I add my portfolio or social links?**
A: Not in the prompt data, but we welcome you to mention them in PR descriptions. Featured contributors may be highlighted.

**Q: What license do my contributions use?**
A: By submitting, you grant WenceStudio by SmartDesign a perpetual, worldwide, royalty-free right to use, modify, publish, and distribute your contribution as part of the library under the [WenceStudio Library License](LICENSE), and you confirm you have the right to do so.

---

## 🎯 Contribution Tiers

### Tier 1: Single Prompt 🌱
- 1 new prompt with testing
- Gets you featured in next release

### Tier 2: Prompt Pack 🌿
- 5-10 related prompts in a category
- Recognized as contributor in README

### Tier 3: Major Feature 🌳
- New category, template, or workflow
- Co-author credit and attribution

---

## 🚀 Getting Help

- 💬 **Questions?** Open a Discussion
- 🐛 **Found a bug?** File an Issue
- 📧 **Direct contact?** Check repo for contact info
- 🤝 **Want to collaborate?** DM or email

---

## ✨ Code of Conduct

We're committed to providing a welcoming, inclusive community.

**Be respectful, constructive, and professional.**
- No harassment or discrimination
- No spam or self-promotion spam
- Focus on the work, not the person
- Help others improve their contributions

---

<div align="center">

### Thank You! 🙏

**Every contribution makes this library better for creators worldwide.**

Whether it's a single prompt, bug fix, or feature suggestion—your effort matters.

**Ready to contribute?** [Create an Issue or PR](https://github.com/Wence412/chatgpt-image-prompt-packs)

**Questions first?** [Start a Discussion](https://github.com/Wence412/chatgpt-image-prompt-packs/discussions)

---

Made with 💜 **WenceStudio by SmartDesign** | **GPT Image Prompt Packs**

</div>
