export class ResultModel {

  constructor(public average_rating: number,
              public directors: string[],
              public genres: string[],
              public primary_title: string,
              public principals: string[],
              public runtime_minutes: number,
              public tid: number,
              public year: number) {
  }
}
