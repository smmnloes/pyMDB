export class BasicDataModel {

  constructor(public average_rating: number,
              public directors: string[],
              public writers: string[],
              public genres: string[],
              public primary_title: string,
              public principals: string[],
              public runtime_minutes: number,
              public tid: number,
              public year: number) {
  }
}
