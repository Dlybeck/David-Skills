# Pipeline checks

Use this when you create or change a build, CI, release, or deploy pipeline. The aim: one
release runs each expensive check once, and nothing reruns it by accident.

1. **Check the host's build tool before writing build files.** A pattern that is correct on one
   tool can be slow or wrong on another. For Docker, run `docker buildx version`: if it fails, the
   host uses the legacy builder, which runs every stage from the top of the Dockerfile down to the
   target and does not skip stages the target does not need. Record what you found in the repo,
   next to the build files or in their docs.
2. **Build exactly what ships.** In a multi-stage Dockerfile, put the shipped stage before any
   test or lint stage, and always build it with an explicit `--target`. That is correct under
   both BuildKit and the legacy builder. Do not let one test target pull in another test stage
   that a parallel job already runs.
3. **Name one authoritative check per release.** Later steps verify its result (a receipt, a
   digest, a commit status) and never rerun its checks. If a later step must run a check, the gate
   should not also run it.
4. **Test the speed contract as well as the safety contract.** Add a cheap test that fails if,
   for example, the deploy runs tests, the shipped stage moves below a test stage, or the deploy
   drops its explicit target.
5. **Write down the release's time budget.** Make a short table next to the pipeline: each step,
   its expected time, what it runs, and whether it needs the human. If a check appears in two
   rows, remove one. If you cannot fill in the table, the pipeline is not designed yet.
