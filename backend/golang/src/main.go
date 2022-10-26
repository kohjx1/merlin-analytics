package main

import (
	"fmt"
	"math"
	"sort"
	"strings"

	"github.com/xtgo/set"
	"gorgonia.org/tensor"
)

var text = []string{
	"O; 995, what's your emergency?",
	"C; Hi, I think there is a fire at my neighbour's place. There is a lot of smoke coming from the window.",
	"O; Okay, can I get your address?",
	"C; The ppstal code is 530909.",
	"O; So it's 909 Hougang Street 91?",
	"C; Yes that's right.",
	"O; Is anyone injured? Do you need an ambulance?",
	"C; No, I don't think so.",
	"O; Okay, a fire truck is on its way. How may I address you?",
	"O; Okay Jack, evacuate the building as soon as possible. ",
	"C; Okay.",
	"O; Okay, thank you Jack. Goodbye.",
}

type doc []int

func (d doc) IDs() []int { return []int(d) }

func makeCorpus(a []string) (map[string]int, []string) {
	retVal := make(map[string]int)
	invRetVal := make([]string, 0)
	var id int
	for _, s := range a {
		for _, f := range strings.Fields(s) {
			f = strings.ToLower(f)
			if _, ok := retVal[f]; !ok {
				retVal[f] = id
				invRetVal = append(invRetVal, f)
				id++
			}
		}
	}
	return retVal, invRetVal
}

func makeDocuments(a []string, c map[string]int) []Document {
	retVal := make([]Document, 0, len(a))
	for _, s := range a {
		var ts []int
		for _, f := range strings.Fields(s) {
			f = strings.ToLower(f)
			id := c[f]
			ts = append(ts, id)
		}
		retVal = append(retVal, doc(ts))
	}
	return retVal
}

type docScore struct {
	id    int
	score float64
}

type docScores []docScore

func (ds docScores) Len() int           { return len(ds) }
func (ds docScores) Less(i, j int) bool { return ds[i].score < ds[j].score }
func (ds docScores) Swap(i, j int) {
	ds[i].score, ds[j].score = ds[j].score, ds[i].score
	ds[i].id, ds[j].id = ds[j].id, ds[i].id
}

func cosineSimilarity(queryScore []float64, docIDs []int, relVec []float64) docScores {
	// special case
	if len(docIDs) == 1 {
		// even more special case!
		if len(queryScore) == 1 {
			return docScores{
				{docIDs[0], queryScore[0] * relVec[0]},
			}
		}

		q := tensor.New(tensor.WithBacking(queryScore))
		m := tensor.New(tensor.WithBacking(relVec))
		score, err := q.Inner(m)
		if err != nil {
			panic(err)
		}
		return docScores{
			{docIDs[0], score.(float64)},
		}
	}

	m := tensor.New(tensor.WithShape(len(docIDs), len(queryScore)), tensor.WithBacking(relVec))
	q := tensor.New(tensor.WithShape(len(queryScore)), tensor.WithBacking(queryScore))
	dp, err := m.MatVecMul(q)
	if err != nil {
		panic(err)
	}

	m2, err := tensor.Square(m)
	if err != nil {
		panic(err)
	}

	normDocs, err := tensor.Sum(m2, 1)
	if err != nil {
		panic(err)
	}

	normDocs, err = tensor.Sqrt(normDocs)
	if err != nil {
		panic(err)
	}

	q2, err := tensor.Square(q)
	if err != nil {
		panic(err)
	}
	normQt, err := tensor.Sum(q2)
	if err != nil {
		panic(err)
	}
	normQ := normQt.Data().(float64)
	normQ = math.Sqrt(normQ)

	norms, err := tensor.Mul(normDocs, normQ)
	if err != nil {
		panic(err)
	}

	cosineSim, err := tensor.Div(dp, norms)
	if err != nil {
		panic(err)
	}
	csData := cosineSim.Data().([]float64)

	var ds docScores
	for i, id := range docIDs {
		score := csData[i]
		ds = append(ds, docScore{id: id, score: score})
	}
	return ds

}

func contains(query Document, in []Document, tf *TFIDF) (docIDs []int, relVec []float64) {
	q := query.IDs()
	q = set.Ints(q) // unique words only
	for i := range in {
		doc := in[i].IDs()

		var count int
		var relevant []float64
		for _, wq := range q {
		inner:
			for _, wd := range doc {
				if wq == wd {
					count++
					break inner
				}
			}
		}
		if count == len(q) {
			// calculate the score of the doc
			score := tf.Score(in[i])
			// get the  scores of the relevant words
			for _, wq := range q {
			inner2:
				for j, wd := range doc {
					if wd == wq {
						relevant = append(relevant, score[j])
						break inner2
					}
				}
			}
			docIDs = append(docIDs, i)
			relVec = append(relVec, relevant...)
		}
	}
	return
}

func Example() {
	corpus, invCorpus := makeCorpus(text)
	docs := makeDocuments(text, corpus)
	tf := New()

	for _, doc := range docs {
		tf.Add(doc)
	}
	tf.CalculateIDF()

	fmt.Println("IDF:")
	for i, w := range invCorpus {
		fmt.Printf("\t%q: %1.1f\n", w, tf.IDF[i])
		if i >= 10 {
			break
		}
	}

	// now we search

	// "FIRE_KW" is a query
	FIRE_KW_1 := doc{corpus["fire"], corpus["smoke"], corpus["engine"], corpus["black smoke"]}
	//FIRE_KW_2 := doc{corpus["smoke"]}

	MEDICAL_KW_1 := doc{corpus["ambulance"]}
	// MEDICAL_KW_2 := doc{corpus["ambulance"]}

	// step1: score the queries
	fireScore := tf.Score(FIRE_KW_1)
	medicalScore := tf.Score(MEDICAL_KW_1)

	// step2: find the docs that contains the queries.
	// if there are no docs, oops.
	fireDocs, fireRelVec := contains(FIRE_KW_1, docs, tf)
	medicalDocs, medicalRelVec := contains(MEDICAL_KW_1, docs, tf)

	// step3: calculate the cosine similarity
	fireRes := cosineSimilarity(fireScore, fireDocs, fireRelVec)
	medicalRes := cosineSimilarity(medicalScore, medicalDocs, medicalRelVec)

	// step4: sort the results
	sort.Sort(sort.Reverse(fireRes))
	sort.Sort(sort.Reverse(medicalRes))

	fmt.Printf("Relevant Docs to \"FIRE_KW\":\n")
	for _, d := range fireRes {
		fmt.Printf("\tID   : %d\n\tScore: %1.3f\n\tDoc  : %q\n", d.id, d.score, text[d.id])
	}
	fmt.Println("")
	fmt.Printf("Relevant Docs to \"MEDICAL_KW\":\n")
	for _, d := range medicalRes {
		fmt.Printf("\tID   : %d\n\tScore: %1.3f\n\tDoc  : %q\n", d.id, d.score, text[d.id])
	}
	// Output:
	// IDF:
	// 	"call": 2.4
	// 	"me": 1.0
	// 	"ishmael": 2.4
	// 	".": 0.5
	// 	"some": 1.7
	// 	"years": 2.4
	// 	"ago": 2.4
	// 	"--": 1.7
	// 	"never": 2.4
	// 	"mind": 2.4
	// 	"how": 2.4
	// Relevant Docs to "Ishmael":
	//	ID   : 0
	//	Score: 1.437
	//	Doc  : "Call me Ishmael ."
	//
	// Relevant Docs to "whenever i find":
	//	ID   : 5
	//	Score: 0.985
	//	Doc  : "whenever I find myself involuntarily pausing before coffin warehouses , and bringing up the rear of every funeral I meet ; "
	//	ID   : 3
	//	Score: 0.962
	//	Doc  : "Whenever I find myself growing grim about the mouth ; "
}

func main() {
	Example()
}