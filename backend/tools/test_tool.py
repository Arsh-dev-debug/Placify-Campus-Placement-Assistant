"""
test_tool.py — generate_mock_test()

Deterministic question banks keyed by role, difficulty, and target company.
The project keeps a static bank instead of calling the LLM so the mock test
stays fast, consistent, and demo-friendly while still providing a rich pool of
questions for campus placement preparation.
"""
from typing import Dict, List

QUESTION_BANK: Dict[str, Dict[str, List[Dict]]] = {
    "Software Developer": {
        "easy": [
            {"q": "What is the time complexity of binary search?", "a": "O(log n)."},
            {"q": "What does OOP stand for?", "a": "Object-Oriented Programming."},
            {"q": "What is the difference between a stack and a queue?", "a": "A stack follows LIFO while a queue follows FIFO."},
            {"q": "What is a primary key in SQL?", "a": "A column or set of columns that uniquely identifies each row."},
            {"q": "What does HTTP 404 mean?", "a": "The requested resource was not found on the server."},
            {"q": "What is a hash map used for?", "a": "It stores key-value pairs for fast lookup, insert, and delete operations."},
        ],
        "medium": [
            {"q": "Explain the difference between a process and a thread.", "a": "A process is an independent execution unit with its own memory space; a thread is a lighter unit that shares memory within a process."},
            {"q": "What is the difference between an interface and an abstract class in Java?", "a": "An interface defines a contract with only method signatures, while an abstract class can share implementation and state."},
            {"q": "How do you detect and remove duplicates from a list while preserving order?", "a": "Use a seen set and iterate through the list while appending only unseen elements."},
            {"q": "What is ACID in database systems?", "a": "Atomicity, Consistency, Isolation, and Durability."},
            {"q": "Why is a database index useful?", "a": "It speeds up query lookup by reducing the amount of data that must be scanned."},
            {"q": "What is the main purpose of load balancing?", "a": "To distribute incoming requests across multiple servers for reliability and scale."},
            {"q": "What is the difference between SQL JOIN and UNION?", "a": "JOIN combines columns from related rows, while UNION combines rows from matching columns across tables or queries."},
        ],
        "hard": [
            {"q": "How would you design a URL shortener at a high level?", "a": "Generate a unique short key, store the mapping in a database or key-value store, validate collisions, and redirect requests through a lookup service with caching and rate limiting."},
            {"q": "Design a rate limiter for a public API. How would you prevent abuse?", "a": "Use token buckets or leaky buckets, track requests per user or IP, enforce quotas, and add burst controls with TTL-based cache keys."},
            {"q": "Explain a deadlock and how you would prevent it in a database-backed application.", "a": "A deadlock happens when two transactions wait on each other. Prevention includes consistent lock ordering, short transaction scopes, and timeouts."},
            {"q": "How would you design a leaderboard with frequent updates and rankings?", "a": "Store scores in a sorted structure or use a ranking service that updates affected entries incrementally and maintains a cache of top results."},
            {"q": "How would you scale a notification system for millions of users?", "a": "Use asynchronous workers, queues, batching, retries, backoff policies, and fan-out strategies with DB and cache separation."},
            {"q": "What is the difference between consistent hashing and regular hashing for distributed systems?", "a": "Consistent hashing minimizes re-sharding when nodes are added or removed by mapping keys across a ring instead of a fixed partition layout."},
        ],
    },
    "Data Analyst": {
        "easy": [
            {"q": "Which SQL clause is used to filter grouped results?", "a": "HAVING."},
            {"q": "What is a primary key in a database?", "a": "It uniquely identifies each record in a table."},
            {"q": "What does ETL stand for?", "a": "Extract, Transform, Load."},
            {"q": "What is a pivot table used for?", "a": "It summarizes and reorganizes data for quick analytical reporting."},
            {"q": "What is the most common measure of central tendency?", "a": "The mean, though median is useful for skewed data."},
        ],
        "medium": [
            {"q": "What is the difference between INNER JOIN and LEFT JOIN?", "a": "INNER JOIN returns only matching rows, while LEFT JOIN returns all rows from the left table with NULLs where the right table has no match."},
            {"q": "What is the difference between RANK() and DENSE_RANK() in SQL?", "a": "RANK() leaves gaps between tied values, while DENSE_RANK() keeps consecutive ranks."},
            {"q": "How do you handle missing values in a dataset?", "a": "Identify the pattern, decide whether to impute, drop, or flag values based on data context, and document the choice."},
            {"q": "Why is data normalization important before model building?", "a": "It brings features to a common scale so learning algorithms converge faster and behave more consistently."},
            {"q": "Explain overfitting in a machine learning model.", "a": "A model learns noise or irrelevant patterns from training data and performs poorly on unseen data."},
            {"q": "What is the purpose of a window function in SQL?", "a": "It allows calculations across a set of rows related to the current row without collapsing the result set."},
        ],
        "hard": [
            {"q": "How would you detect and handle outliers in a large sales dataset?", "a": "Use IQR or z-score for flagging, validate business impact, and then decide whether to cap, transform, or remove the outliers depending on context."},
            {"q": "Explain how you would design an A/B test for a product improvement.", "a": "Randomize users into groups, define success metrics and statistical significance thresholds, monitor for bias, and compare outcomes with confidence intervals."},
            {"q": "What is cohort analysis and why is it useful?", "a": "Cohort analysis groups users by shared attributes over time to reveal retention and behavioral patterns."},
            {"q": "How would you reduce skew in a highly imbalanced classification problem?", "a": "Apply resampling, cost-sensitive learning, better metrics like PR-AUC, and focus on business trade-offs before deciding on a threshold."},
            {"q": "Explain how you would validate a forecasting model.", "a": "Use time-series backtesting, compare against baseline models, check residuals, and measure MAE, RMSE, and MAPE on holdout periods."},
        ],
    },
    "AI/ML Engineer": {
        "easy": [
            {"q": "What is supervised learning?", "a": "Training a model on labeled examples to learn mappings from inputs to outputs."},
            {"q": "What is the purpose of a loss function?", "a": "It measures how far the model prediction is from the expected output."},
            {"q": "What is the role of an activation function in a neural network?", "a": "It introduces non-linearity so the network can model complex patterns."},
            {"q": "What is a confusion matrix?", "a": "It summarizes model predictions against ground truth for classification problems."},
            {"q": "What is the difference between precision and recall?", "a": "Precision captures the correctness of positive predictions; recall measures how many true positives were found."},
        ],
        "medium": [
            {"q": "What is the difference between bias and variance?", "a": "Bias is underfitting; variance is overfitting. A balanced model minimizes both."},
            {"q": "Explain gradient descent in one sentence.", "a": "It iteratively updates model parameters in the direction that reduces the loss function."},
            {"q": "Why do we use train/validation/test splits?", "a": "To tune and evaluate the model without leaking data and overstating performance."},
            {"q": "What is the difference between L1 and L2 regularization?", "a": "L1 encourages sparse features via absolute-value penalties, while L2 penalizes large weights using squared penalties."},
            {"q": "What is cross-validation used for?", "a": "It estimates how well the model generalizes by training and validating on multiple data folds."},
        ],
        "hard": [
            {"q": "How would you explain the vanishing gradient problem and how to mitigate it?", "a": "Deep networks can fail to learn when gradients become too small. Mitigation includes ReLU activations, good initialization, normalization, and residual connections."},
            {"q": "Why is attention useful in transformer models?", "a": "It lets the model weigh the importance of different tokens in sequence data, enabling better context handling."},
            {"q": "How would you design a recommendation system for millions of users?", "a": "Use candidate generation, collaborative filtering, embedding models, online scoring, click-through optimization, and real-time feedback loops with dense retrieval and ranking stages."},
            {"q": "How do you handle class imbalance in a fraud detection model?", "a": "Use cost-sensitive learning, oversampling, threshold tuning, and metrics like precision-recall curves rather than raw accuracy."},
            {"q": "What is the difference between batch normalization and layer normalization?", "a": "Batch normalization normalizes across a batch, while layer normalization normalizes across features within each sample."},
        ],
    },
    "Frontend Developer": {
        "easy": [
            {"q": "What is the purpose of CSS flexbox?", "a": "It is used to layout elements in rows or columns with efficient alignment and spacing."},
            {"q": "What is the DOM?", "a": "The Document Object Model is the browser representation of the page structure."},
            {"q": "What does event bubbling mean in JavaScript?", "a": "An event triggered on a child element propagates up through ancestor elements."},
        ],
        "medium": [
            {"q": "What is the difference between == and === in JavaScript?", "a": "== performs type coercion, while === compares both type and value."},
            {"q": "What is the purpose of a debounced input handler?", "a": "It reduces the frequency of function calls during rapid user input, commonly used for search fields."},
            {"q": "How do you optimize a large React rendering tree?", "a": "Use memoization, code splitting, lazy loading, and keeping state local to the components that need it."},
        ],
        "hard": [
            {"q": "How would you design a scalable dashboard UI with frequent real-time updates?", "a": "Use efficient rendering, data virtualization, throttled updates, websockets, and normalized state management."},
            {"q": "What is the difference between CSR and SSR in web apps?", "a": "Client-side rendering builds the interface in the browser, while server-side rendering generates HTML on the server for faster initial paint and SEO."},
        ],
    },
    "DevOps Engineer": {
        "easy": [
            {"q": "What is a container?", "a": "A lightweight, isolated environment that packages an application and its dependencies."},
            {"q": "What is the purpose of CI/CD?", "a": "To automate build, test, and deployment pipelines for faster and safer releases."},
            {"q": "What does Docker do?", "a": "It packages applications into portable containers that run consistently across environments."},
        ],
        "medium": [
            {"q": "What is the main difference between a virtual machine and a container?", "a": "A VM includes a full guest OS, while a container shares the host OS kernel and uses fewer resources."},
            {"q": "Why is infrastructure as code useful?", "a": "It makes environment setup consistent, repeatable, and auditable through declarative configuration."},
            {"q": "What is the role of Kubernetes?", "a": "It orchestrates containerized workloads across nodes with scheduling, scaling, and self-healing features."},
        ],
        "hard": [
            {"q": "How would you design a zero-downtime deployment strategy?", "a": "Use rolling upgrades, health checks, readiness probes, canary releases, and blue-green deployment patterns."},
            {"q": "What would you monitor to ensure a production service is healthy?", "a": "Latency, error rate, saturation, throughput, logs, traces, and resource utilization for both infrastructure and app code."},
        ],
    },
}

COMPANY_QUESTION_BANK: Dict[str, Dict[str, List[Dict]]] = {
    "Microsoft": {
        "easy": [
            {"q": "Which data structure is typically used in BFS?", "a": "Queue."},
            {"q": "What does SOLID stand for?", "a": "Single Responsibility, Open/Closed, Liskov Substitution, Interface Segregation, Dependency Inversion."},
            {"q": "What is the purpose of caching?", "a": "To reduce repeated expensive computation or data retrieval."},
            {"q": "What is the difference between HTTP and HTTPS?", "a": "HTTPS adds TLS/SSL encryption for secure communication."},
        ],
        "medium": [
            {"q": "How would you find the first non-repeating character in a string?", "a": "Count frequencies and return the first entry with a count of one."},
            {"q": "What is the difference between an interface and an abstract class?", "a": "An interface is a contract; an abstract class can include shared implementations and state."},
            {"q": "How would you design a caching layer for a high-traffic system?", "a": "Use a distributed cache with invalidation rules, TTLs, hot-key tracking, and fallback to the primary datastore."},
            {"q": "What is the purpose of a load balancer in a distributed system?", "a": "It spreads traffic across healthy instances to improve availability and fault tolerance."},
        ],
        "hard": [
            {"q": "Design a URL shortener and explain how you would scale it.", "a": "Use a compact encoded key, a durable mapping store, hash-based lookup, load balancing, caching, and conflict handling for collisions and regional scale."},
            {"q": "What is the difference between horizontal and vertical scaling?", "a": "Horizontal scaling adds more machines; vertical scaling increases the power of a single machine."},
            {"q": "How would you build a distributed rate limiter?", "a": "Use centralized token buckets, distributed counters, or a consistent hashing approach with Redis or a sharded service."},
            {"q": "How would you design a search ranking system?", "a": "Combine query understanding, document retrieval, ranking features, machine learning scoring, and freshness/quality heuristics."},
        ],
    },
    "Amazon": {
        "easy": [
            {"q": "What is the average time complexity of a hash table lookup?", "a": "O(1) on average."},
            {"q": "What is idempotency in APIs?", "a": "Repeated requests produce the same result without causing duplicate side effects."},
            {"q": "What is the purpose of a queue in distributed systems?", "a": "It decouples producers and consumers and smooths load spikes."},
            {"q": "What does CAP theorem say?", "a": "A distributed system cannot simultaneously guarantee consistency, availability, and partition tolerance."},
        ],
        "medium": [
            {"q": "How would you find the top K frequent elements in a stream?", "a": "Use a hashmap to count and a min-heap or bucket strategy for top-K selection."},
            {"q": "How do you make an API resilient to duplicate requests?", "a": "Use idempotency keys, deduplication, and safe retry semantics."},
            {"q": "Explain the trade-off between consistency and availability.", "a": "In partitioned systems, stronger consistency usually reduces availability, and vice versa."},
            {"q": "How would you design a highly available order processing system?", "a": "Use durable queues, idempotent handlers, retries, app-level validation, and queue-based worker scaling."},
        ],
        "hard": [
            {"q": "Design an order-processing pipeline for millions of daily orders.", "a": "Use asynchronous event-driven components, idempotent processing, queue durability, partitioned consumers, retries, monitoring, and decoupled storage."},
            {"q": "What is eventual consistency?", "a": "Replicas converge over time rather than instantaneously, allowing higher availability and partition tolerance."},
            {"q": "How would you handle hot keys in a distributed cache?", "a": "Use sharding, caching strategies, request deduplication, and partial precomputation for repeated data access."},
            {"q": "How do you design a recommendation engine for a storefront?", "a": "Generate candidate products, rank by user affinity and popularity, and optimize using online experimentation and user-feedback loops."},
        ],
    },
    "Google": {
        "easy": [
            {"q": "What is a map in programming?", "a": "A data structure that stores key-value pairs for lookup by key."},
            {"q": "Why is Big-O useful?", "a": "It describes how runtime or memory grows as input size increases."},
            {"q": "What is a trie used for?", "a": "It efficiently stores and searches strings such as prefixes or dictionary words."},
            {"q": "What is the purpose of a graph?", "a": "It models relationships between entities such as users, pages, or routes."},
        ],
        "medium": [
            {"q": "How do you detect whether a string is a palindrome?", "a": "Compare characters from both ends while ignoring non-alphanumeric characters if needed."},
            {"q": "Explain how you would optimize a search query with millions of records.", "a": "Use indexed search, filter pruning, relevancy scoring, and caching for high-frequency query patterns."},
            {"q": "What is the difference between DFS and BFS?", "a": "DFS goes deep before broad; BFS explores level by level and is often used for shortest paths in unweighted graphs."},
            {"q": "What is the purpose of a priority queue?", "a": "It allows quick access to the smallest or largest item based on priority."},
        ],
        "hard": [
            {"q": "How would you design a distributed search engine?", "a": "Use a retrieval layer, inverted indexes, sharding, relevance scoring, caching, consistent hashing, and faceted filters for scale and performance."},
            {"q": "How do you find the shortest path in a weighted graph efficiently?", "a": "Use Dijkstra's algorithm for non-negative weights or Bellman-Ford for graphs with negative edges."},
            {"q": "How would you build a crawler that scales to the web?", "a": "Use polite crawling, queue scheduling, deduplication, content extraction, indexing pipelines, and distributed workers."},
            {"q": "What are the trade-offs between SQL and NoSQL for product search?", "a": "SQL offers consistency and relational joins, while NoSQL offers flexible scale and faster horizontal distribution for large unstructured data."},
        ],
    },
    "Meta": {
        "easy": [
            {"q": "What is a feed?", "a": "A real-time or near-real-time stream of updates ranked by relevance or recency."},
            {"q": "What is a social graph?", "a": "It represents relationships between users, communities, and content."},
            {"q": "Why is caching important in a social product?", "a": "It reduces latency and database load for repeated data access."},
        ],
        "medium": [
            {"q": "How would you reduce feed latency for a large user base?", "a": "Use precomputed ranking, edge caches, asynchronous updates, and partitioning of user timelines."},
            {"q": "How would you design a notification system for events across a social network?", "a": "Use fan-out workers, message queues, delivery retries, and user preference filtering."},
            {"q": "What is the role of recommendation in content ranking?", "a": "It personalizes content selection based on user behavior, similarity, and historical engagement."},
        ],
        "hard": [
            {"q": "Design a social feed service for billions of posts and a highly personalized ranking model.", "a": "Use graph-based recommendations, ranking services, distributed caches, stream processing, and online experimentation to maintain freshness and quality."},
            {"q": "How would you design a notification deduplication system for millions of events?", "a": "Use event IDs, batching, TTL-based dedupe windows, and idempotent delivery pipelines."},
            {"q": "What trade-offs would you consider when designing live notifications for real-time engagement?", "a": "Balance freshness, rate limits, push volume, user preference filtering, and infrastructure cost."},
        ],
    },
    "TCS": {
        "easy": [
            {"q": "What is the difference between a compiler and an interpreter?", "a": "A compiler translates the whole program before execution; an interpreter executes code line-by-line."},
            {"q": "What is normalization in a relational database?", "a": "It organizes data to reduce redundancy and inconsistency."},
            {"q": "What is the use of a foreign key?", "a": "It links records in one table to records in another table."},
        ],
        "medium": [
            {"q": "What SQL concept combines rows from two related tables?", "a": "JOIN."},
            {"q": "What is the difference between DELETE and TRUNCATE in SQL?", "a": "DELETE removes rows with logging and can be rolled back; TRUNCATE removes all rows faster but is less granular."},
            {"q": "How would you design a scalable student result-processing system?", "a": "Use asynchronous processing, validation, separate services, and monitoring for batch and per-student updates."},
        ],
        "hard": [
            {"q": "How would you build an attendance and assessment tracking system for a college campus?", "a": "Use transactional data storage, event-driven processing, approvals, dashboarding, and role-based access control."},
            {"q": "How do you ensure reliability in a campus management application with concurrent users?", "a": "Use transaction isolation, optimistic locking, queue-backed async jobs, backups, and monitoring for service health."},
        ],
    },
    "Infosys": {
        "easy": [
            {"q": "What is a variable in programming?", "a": "A named storage location used to hold data."},
            {"q": "What is an array?", "a": "A collection of similar data items stored in contiguous memory."},
            {"q": "What is recursion?", "a": "A function calling itself to solve smaller subproblems."},
        ],
        "medium": [
            {"q": "Why is sorting important in software engineering?", "a": "It helps organize data for faster searching and efficient processing."},
            {"q": "What is the difference between a list and a set?", "a": "A list preserves order and duplicates, while a set stores unique values without preserving order."},
            {"q": "What is a thread-safe operation?", "a": "One that can be safely accessed by multiple threads without causing race conditions."},
        ],
        "hard": [
            {"q": "How would you design a file synchronization system?", "a": "Use file hashing, change detection, retries, conflict resolution, and queue-based updates."},
            {"q": "How do you improve performance in a system with repeated database reads?", "a": "Add caching, batch queries, index management, and read-through patterns with monitoring for stale entries."},
        ],
    },
    "Accenture": {
        "easy": [
            {"q": "What is cloud computing?", "a": "It delivers computing resources such as storage, networking, and compute over the internet."},
            {"q": "What is API integration?", "a": "It connects different software systems so they can exchange data and functionality."},
            {"q": "What is a microservice?", "a": "A small, independently deployable service focused on one business capability."},
        ],
        "medium": [
            {"q": "What is the difference between synchronous and asynchronous processing?", "a": "Synchronous processing waits before continuing, while asynchronous processing allows parallel work and later completion."},
            {"q": "Why would you use a message broker?", "a": "To decouple services, buffer load spikes, and support async communication."},
            {"q": "What is the purpose of caching in distributed web applications?", "a": "To reduce database load and improve response time for repeated requests."},
        ],
        "hard": [
            {"q": "How would you design a cloud-native enterprise integration platform?", "a": "Use API gateways, event buses, service discovery, observability, authentication, retries, and circuit breakers."},
            {"q": "How do you manage reliable data synchronization between many systems?", "a": "Use event sourcing, idempotent consumers, timestamps or versioning, and reconciliation jobs."},
        ],
    },
    "Goldman Sachs": {
        "easy": [
            {"q": "What is a financial market?", "a": "A place where buyers and sellers trade financial instruments such as stocks, bonds, and currencies."},
            {"q": "What is risk in finance?", "a": "The chance of losing value due to market, credit, or operational factors."},
            {"q": "What is a portfolio?", "a": "A collection of investments held by an individual or organization."},
        ],
        "medium": [
            {"q": "What is the difference between a stock and a bond?", "a": "A stock represents ownership in a company, while a bond is a debt instrument that pays periodic interest."},
            {"q": "What is VaR?", "a": "Value at Risk estimates the maximum expected loss over a period for a given confidence level."},
            {"q": "Why is data quality critical in trading systems?", "a": "Inaccurate or late data can lead to poor decision-making and serious financial losses."},
        ],
        "hard": [
            {"q": "How would you design a risk monitoring system for a trading platform?", "a": "Aggregate live market data, compute exposure and limit breaches, trigger alerts, and provide dashboards with lineage and auditability."},
            {"q": "What factors contribute to systemic risk in finance?", "a": "Interconnected exposures, leverage, liquidity shortages, and correlated market shocks across institutions."},
        ],
    },
    "Oracle": {
        "easy": [
            {"q": "What is SQL?", "a": "Structured Query Language used to manage and query relational databases."},
            {"q": "What is a transaction?", "a": "A sequence of database operations executed as a single unit."},
            {"q": "What is indexing in a database?", "a": "A structure that helps locate rows quickly without scanning the whole table."},
        ],
        "medium": [
            {"q": "What is normalization in database design?", "a": "It reduces duplication and improves data integrity by organizing tables logically."},
            {"q": "How do you improve query performance without changing logic?", "a": "Add indexes, rewrite joins, reduce scans, and update statistics where appropriate."},
            {"q": "What is the purpose of a foreign key?", "a": "It links related records across tables and enforces referential integrity."},
        ],
        "hard": [
            {"q": "How would you design a large-scale database solution for analytics workloads?", "a": "Use partitioning, columnar storage, indexing, replication, and optimized ETL pipelines tailored for analytical queries."},
            {"q": "What trade-offs exist between OLTP and OLAP systems?", "a": "OLTP optimizes transactional throughput and consistency, while OLAP optimizes analytical queries across large volumes of historical data."},
        ],
    },
}


def _normalize_key(value: str) -> str:
    return (value or "").strip().casefold()


def generate_mock_test(role: str, difficulty: str = "medium", num_questions: int = 3, company: str = "General") -> List[Dict]:
    normalized_company = _normalize_key(company)
    normalized_role = _normalize_key(role)
    normalized_difficulty = _normalize_key(difficulty)

    company_bank = COMPANY_QUESTION_BANK.get(company or "General")
    if not company_bank:
        company_key = next((key for key in COMPANY_QUESTION_BANK if _normalize_key(key) == normalized_company), None)
        company_bank = COMPANY_QUESTION_BANK.get(company_key)

    if company_bank:
        questions = company_bank.get(normalized_difficulty, company_bank.get("medium", []))
        if questions:
            return questions[: max(1, num_questions)]

    role_key = next((key for key in QUESTION_BANK if _normalize_key(key) == normalized_role), "Software Developer")
    role_bank = QUESTION_BANK.get(role_key, QUESTION_BANK["Software Developer"])
    questions = role_bank.get(normalized_difficulty, role_bank.get("medium", []))
    return questions[: max(1, num_questions)] if questions else []


def score_mock_test(answers: List[Dict]) -> float:
    """answers: list of {"correct": bool}. Returns percentage score."""
    if not answers:
        return 0.0
    correct = sum(1 for a in answers if a.get("correct"))
    return round(correct / len(answers) * 100, 1)
