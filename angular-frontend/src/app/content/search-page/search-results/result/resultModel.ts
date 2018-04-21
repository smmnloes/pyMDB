export class resultModel {

  constructor(public averageRating: number,
              public directors: string[],
              public genres: string[],
              public primaryTitle: string,
              public principals: string[],
              public runtimeMinutes: number,
              public tid: string,
              public year: number) {
  }
}
